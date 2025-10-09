output "invoke_url" {
  description = "Base invoke URL for the REST API stage"
  value       = "https://${aws_api_gateway_rest_api.this.id}.execute-api.${var.aws_region}.amazonaws.com/${aws_api_gateway_stage.stage.stage_name}"
}

output "api_key_id" {
  description = "REST API key ID"
  value       = aws_api_gateway_api_key.default.id
}

output "api_key_value" {
  description = "REST API key value (sensitive)"
  value       = aws_api_gateway_api_key.default.value
  sensitive   = true
}

output "resource_path_example" {
  description = "Resource path that requires applicationId"
  value       = "/apps/{applicationId}"
}
