variable "aws_region" {
  type    = string
  default = "ap-northeast-1"
}

variable "api_name" {
  type    = string
  default = "account-p-rest"
}

variable "stage_name" {
  type    = string
  default = "prod"
}

variable "lambda_function_name" {
  type    = string
  default = "account-p-logger"
}

variable "apigw_access_log_retention_days" {
  type    = number
  default = 30
}
