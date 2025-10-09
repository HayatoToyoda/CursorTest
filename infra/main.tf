terraform {
  required_version = ">= 1.3.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.4"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Package Lambda from local source directory
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../lambda_src"
  output_path = "${path.module}/lambda.zip"
}

# Lambda execution role
resource "aws_iam_role" "lambda_exec" {
  name = "${var.api_name}-${var.stage_name}-lambda-exec"
  assume_role_policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic_logs" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Lambda function
resource "aws_lambda_function" "app" {
  function_name = var.lambda_function_name
  role          = aws_iam_role.lambda_exec.arn
  handler       = "app.handler"
  runtime       = "python3.11"

  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  publish = true

  environment {
    variables = {
      LOG_LEVEL = "INFO"
    }
  }
}

# REST API (API Gateway v1)
resource "aws_api_gateway_rest_api" "this" {
  name           = var.api_name
  api_key_source = "HEADER"
  endpoint_configuration { types = ["REGIONAL"] }
}

# Resources: /apps/{applicationId}
resource "aws_api_gateway_resource" "apps" {
  rest_api_id = aws_api_gateway_rest_api.this.id
  parent_id   = aws_api_gateway_rest_api.this.root_resource_id
  path_part   = "apps"
}

resource "aws_api_gateway_resource" "application" {
  rest_api_id = aws_api_gateway_rest_api.this.id
  parent_id   = aws_api_gateway_resource.apps.id
  path_part   = "{applicationId}"
}

# Validate that path param is present
resource "aws_api_gateway_request_validator" "validate_params" {
  name                        = "validate-params"
  rest_api_id                 = aws_api_gateway_rest_api.this.id
  validate_request_parameters = true
  validate_request_body       = false
}

# Method requiring API Key
resource "aws_api_gateway_method" "any_application" {
  rest_api_id   = aws_api_gateway_rest_api.this.id
  resource_id   = aws_api_gateway_resource.application.id
  http_method   = "ANY"
  authorization = "NONE"

  api_key_required    = true
  request_validator_id = aws_api_gateway_request_validator.validate_params.id
  request_parameters = {
    "method.request.path.applicationId" = true
  }
}

# Proxy integration to Lambda
resource "aws_api_gateway_integration" "lambda_proxy" {
  rest_api_id             = aws_api_gateway_rest_api.this.id
  resource_id             = aws_api_gateway_resource.application.id
  http_method             = aws_api_gateway_method.any_application.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.app.invoke_arn
}

# Deployment and stage with JSON access logs
resource "aws_api_gateway_deployment" "this" {
  rest_api_id = aws_api_gateway_rest_api.this.id

  triggers = {
    redeploy_hash = sha1(jsonencode([
      aws_api_gateway_resource.application.id,
      aws_api_gateway_method.any_application.id,
      aws_api_gateway_integration.lambda_proxy.id
    ]))
  }

  lifecycle {
    create_before_destroy = true
  }

  depends_on = [aws_api_gateway_integration.lambda_proxy]
}

locals {
  access_log_format = "{\n  \"requestTimeEpoch\": $context.requestTimeEpoch,\n  \"requestId\": \"$context.requestId\",\n  \"apiId\": \"$context.apiId\",\n  \"stage\": \"$context.stage\",\n  \"path\": \"$context.path\",\n  \"httpMethod\": \"$context.httpMethod\",\n  \"status\": $context.status,\n  \"responseLatency\": $context.responseLatency,\n  \"integrationStatus\": \"$context.integrationStatus\",\n  \"integrationLatency\": $context.integrationLatency,\n  \"apiKeyId\": \"$context.identity.apiKeyId\",\n  \"authorizerPrincipalId\": \"$context.authorizer.principalId\",\n  \"error\": \"$context.error.messageString\"\n}"
}

resource "aws_cloudwatch_log_group" "apigw_access" {
  name              = "/aws/apigw/${var.api_name}/${var.stage_name}/access"
  retention_in_days = var.apigw_access_log_retention_days
}

resource "aws_api_gateway_stage" "stage" {
  rest_api_id  = aws_api_gateway_rest_api.this.id
  deployment_id = aws_api_gateway_deployment.this.id
  stage_name   = var.stage_name

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.apigw_access.arn
    format          = local.access_log_format
  }
  depends_on = [aws_api_gateway_account.account]
}

# Optional: method settings for metrics/logging level
resource "aws_api_gateway_method_settings" "all" {
  rest_api_id = aws_api_gateway_rest_api.this.id
  stage_name  = aws_api_gateway_stage.stage.stage_name
  method_path = "*/*"
  settings {
    metrics_enabled = true
    logging_level   = "INFO"
    data_trace_enabled = false
  }
}

# API Gateway account-level CloudWatch role for logs
resource "aws_iam_role" "apigw_cloudwatch" {
  name = "${var.api_name}-${var.stage_name}-apigw-cw"
  assume_role_policy = jsonencode({
    Version   = "2012-10-17",
    Statement = [{
      Effect    = "Allow",
      Principal = { Service = "apigateway.amazonaws.com" },
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "apigw_cloudwatch" {
  name = "${var.api_name}-${var.stage_name}-apigw-cw"
  role = aws_iam_role.apigw_cloudwatch.id
  policy = jsonencode({
    Version   = "2012-10-17",
    Statement = [{
      Effect   = "Allow",
      Action   = [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:DescribeLogGroups",
        "logs:DescribeLogStreams",
        "logs:PutLogEvents",
        "logs:GetLogEvents",
        "logs:FilterLogEvents"
      ],
      Resource = "*"
    }]
  })
}

resource "aws_api_gateway_account" "account" {
  cloudwatch_role_arn = aws_iam_role.apigw_cloudwatch.arn
}

# Permission for API Gateway to invoke Lambda
resource "aws_lambda_permission" "apigw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.app.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.this.execution_arn}/*/*/*"
}

# API Key and Usage Plan
resource "aws_api_gateway_api_key" "default" {
  name    = "${var.api_name}-${var.stage_name}-key"
  enabled = true
}

resource "aws_api_gateway_usage_plan" "plan" {
  name = "${var.api_name}-${var.stage_name}-plan"

  api_stages {
    api_id = aws_api_gateway_rest_api.this.id
    stage  = aws_api_gateway_stage.stage.stage_name
  }
}

resource "aws_api_gateway_usage_plan_key" "attach" {
  key_id        = aws_api_gateway_api_key.default.id
  key_type      = "API_KEY"
  usage_plan_id = aws_api_gateway_usage_plan.plan.id
}
