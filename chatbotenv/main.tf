locals {
    tags = {
    managed-by  = "terraform"
    Environment = var.env
    region      = "us-east-1"
    ProductCode = var.product_code
  }
  product = var.product_code
  env     = var.env
  vpc_cidr = "10.0.0.0/16"
  s3_origin_id = "chatbotenv-apps"
  s3aibot_origin_id = "aibot-chatbotenv-apps"
  prefix = "chatbotenv"
  chatbotenv_appcode = "chatbotenv"
}

# Iterate over lambda functions and conditionally add them to respective APIs
locals {
  lambda_log_level = "INFO"
   rest_lambda_functions = { for k, v in var.chatbotenv_lambda_functions : k => v if v.api_type == "REST" }
   websocket_lambda_functions = { for k, v in var.chatbotenv_lambda_functions : k => v if v.api_type == "WEBSOCKET" }
   rest_cors_lambda_functions = { for k, v in var.chatbotenv_lambda_functions : k => v if v.api_type == "REST_CORS" }
  lambda_with_s3_trigger = { for k, v in var.chatbotenv_lambda_functions : k => v if v.s3_trigger != null }
  common_lambda_environment_vars = merge(local.bucket_names_map,local.table_names_map,{"logging_level"=local.lambda_log_level,"Chatbot_log_group"= aws_cloudwatch_log_group.chabot_log_group.name})
}


provider "aws" {
  region = var.region
}

