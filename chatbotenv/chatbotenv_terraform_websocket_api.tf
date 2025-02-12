
data "archive_file" "ws_connect_lambda_archive" {
    for_each      = var.websocket_apis
    type          = "zip"
    source_dir    = "${path.module}/source/${each.value.connect_lambda_template}"
    output_path   = "${path.module}/source/archive/${each.value.connect_lambda_template}.zip"
}

resource "aws_lambda_function" "ws_connect_lambda" {
    for_each          = var.websocket_apis
    function_name     = "${local.prefix}-${each.key}-connect"
    filename          = data.archive_file.ws_connect_lambda_archive[each.key].output_path
    source_code_hash  = data.archive_file.ws_connect_lambda_archive[each.key].output_base64sha256
    runtime           = "python3.10"
    handler           = "lambda_function.lambda_handler"
    publish           = true
    role              = aws_iam_role.chatbotenv_lambda_role.arn
    # logging_config {
    #       application_log_level = "INFO"
    #       system_log_level = "WARN"
    #       log_format = "JSON"
    #       log_group = aws_cloudwatch_log_group.chabot_log_group.name
    #     }
    environment {
        variables = merge(local.common_lambda_environment_vars,
                        each.value.additional_env_variables,
                        {"api_gateway_mgmt_url" = replace(aws_apigatewayv2_stage.ws_messenger_api_stage[each.key].invoke_url,"wss://","https://")})
    }
    tags = local.tags
}

data "archive_file" "ws_disconnect_lambda_archive" {
    for_each      = var.websocket_apis
    type          = "zip"
    source_dir    = "${path.module}/source/${each.value.disconnect_lambda_template}"
    output_path   = "${path.module}/source/archive/${each.value.disconnect_lambda_template}.zip"
}

resource "aws_lambda_function" "ws_disconnect_lambda" {
    for_each          = var.websocket_apis
    function_name     = "${local.prefix}-${each.key}-disconnect"
    filename          = data.archive_file.ws_disconnect_lambda_archive[each.key].output_path
    source_code_hash  = data.archive_file.ws_disconnect_lambda_archive[each.key].output_base64sha256
    runtime           = "python3.10"
    handler           = "lambda_function.lambda_handler"
    publish           = true
    role              = aws_iam_role.chatbotenv_lambda_role.arn
    # logging_config {
    #       application_log_level = "INFO"
    #       system_log_level = "WARN"
    #       log_format = "JSON"
    #       log_group = aws_cloudwatch_log_group.chabot_log_group.name
    #     }
    environment {
        variables = merge(local.common_lambda_environment_vars,
                        each.value.additional_env_variables,
                        {"api_gateway_mgmt_url" = replace(aws_apigatewayv2_stage.ws_messenger_api_stage[each.key].invoke_url,"wss://","https://")})
    }
    tags = local.tags
}

data "archive_file" "ws_message_lambda_archive" {
    for_each      = var.websocket_apis
    type          = "zip"
    source_dir    = "${path.module}/source/${each.value.message_lambda_template}"
    output_path   = "${path.module}/source/archive/${each.value.message_lambda_template}.zip"
}

resource "aws_cloudwatch_log_group" "chabot_log_group" {
  name              = "/aws/lambda/chatbot/${local.prefix}_chatbot_event_logs"
  retention_in_days = 3
  tags = local.tags
}

resource "aws_lambda_function" "ws_message_lambda" {
    for_each          = var.websocket_apis
    function_name     = "${local.prefix}-${each.key}-message"
    filename          = data.archive_file.ws_message_lambda_archive[each.key].output_path
    source_code_hash  = data.archive_file.ws_message_lambda_archive[each.key].output_base64sha256
    #layers           = ["arn:aws:lambda:us-east-1:685363273140:layer:boto3-1-3-152_latest:2"]
    runtime           = "python3.10"
    handler           = "lambda_function.lambda_handler"
    timeout           = each.value.timeout
    publish           = true
    role              = aws_iam_role.chatbotenv_lambda_role.arn
    # logging_config {
    #       application_log_level = "INFO"
    #       system_log_level = "WARN"
    #       log_format = "JSON"
    #       log_group = aws_cloudwatch_log_group.chabot_log_group.name
    #     }
    environment {
        variables = merge(local.common_lambda_environment_vars,
                        each.value.additional_env_variables,
                        {"api_gateway_mgmt_url" = replace(aws_apigatewayv2_stage.ws_messenger_api_stage[each.key].invoke_url,"wss://","https://")})
    }

    tags = local.tags
}

resource "aws_apigatewayv2_api" "ws_messenger_api_gateway" {
    for_each                   = var.websocket_apis
    name                       = each.key
    protocol_type              = "WEBSOCKET"
    route_selection_expression = "$request.body.action"
    tags = local.tags
}

resource "aws_apigatewayv2_integration" "ws_messenger_api_integration" {
    for_each                  = var.websocket_apis
    api_id                    = aws_apigatewayv2_api.ws_messenger_api_gateway[each.key].id
    integration_type          = "AWS_PROXY"
    integration_uri           = aws_lambda_function.ws_message_lambda[each.key].invoke_arn
    credentials_arn           = aws_iam_role.chatbotenv_lambda_role.arn
    content_handling_strategy = "CONVERT_TO_TEXT"
    passthrough_behavior      = "WHEN_NO_MATCH"
}

resource "aws_apigatewayv2_integration_response" "ws_messenger_api_integration_response" {
    for_each                 = var.websocket_apis
    api_id                   = aws_apigatewayv2_api.ws_messenger_api_gateway[each.key].id
    integration_id           = aws_apigatewayv2_integration.ws_messenger_api_integration[each.key].id
    integration_response_key = "/200/"
}

resource "aws_apigatewayv2_integration" "ws_connect_api_integration" {
    for_each                  = var.websocket_apis
    api_id                    = aws_apigatewayv2_api.ws_messenger_api_gateway[each.key].id
    integration_type          = "AWS_PROXY"
    integration_uri           = aws_lambda_function.ws_connect_lambda[each.key].invoke_arn
    credentials_arn           = aws_iam_role.chatbotenv_lambda_role.arn
    content_handling_strategy = "CONVERT_TO_TEXT"
    passthrough_behavior      = "WHEN_NO_MATCH"
}

resource "aws_apigatewayv2_integration_response" "ws_connect_api_integration_response" {
    for_each                 = var.websocket_apis
    api_id                   = aws_apigatewayv2_api.ws_messenger_api_gateway[each.key].id
    integration_id           = aws_apigatewayv2_integration.ws_connect_api_integration[each.key].id
    integration_response_key = "/200/"
}

resource "aws_apigatewayv2_integration" "ws_disconnect_api_integration" {
    for_each                  = var.websocket_apis
    api_id                    = aws_apigatewayv2_api.ws_messenger_api_gateway[each.key].id
    integration_type          = "AWS_PROXY"
    integration_uri           = aws_lambda_function.ws_disconnect_lambda[each.key].invoke_arn
    credentials_arn           = aws_iam_role.chatbotenv_lambda_role.arn
    content_handling_strategy = "CONVERT_TO_TEXT"
    passthrough_behavior      = "WHEN_NO_MATCH"
}

resource "aws_apigatewayv2_integration_response" "ws_disconnect_api_integration_response" {
    for_each                 = var.websocket_apis
    api_id                   = aws_apigatewayv2_api.ws_messenger_api_gateway[each.key].id
    integration_id           = aws_apigatewayv2_integration.ws_disconnect_api_integration[each.key].id
    integration_response_key = "/200/"
}

resource "aws_apigatewayv2_route" "ws_messenger_api_default_route" {
    for_each  = var.websocket_apis
    api_id    = aws_apigatewayv2_api.ws_messenger_api_gateway[each.key].id
    route_key = "$default"
    target    = "integrations/${aws_apigatewayv2_integration.ws_messenger_api_integration[each.key].id}"
}

resource "aws_apigatewayv2_route" "ws_messenger_api_connect_route" {
    for_each  = var.websocket_apis
    api_id    = aws_apigatewayv2_api.ws_messenger_api_gateway[each.key].id
    route_key = "$connect"
    target    = "integrations/${aws_apigatewayv2_integration.ws_connect_api_integration[each.key].id}"
}

resource "aws_apigatewayv2_route" "ws_messenger_api_disconnect_route" {
    for_each  = var.websocket_apis
    api_id    = aws_apigatewayv2_api.ws_messenger_api_gateway[each.key].id
    route_key = "$disconnect"
    target    = "integrations/${aws_apigatewayv2_integration.ws_disconnect_api_integration[each.key].id}"
}

resource "aws_apigatewayv2_route" "ws_message_api_message_route" {
    for_each  = var.websocket_apis
    api_id    = aws_apigatewayv2_api.ws_messenger_api_gateway[each.key].id
    route_key = each.value.route
    target    = "integrations/${aws_apigatewayv2_integration.ws_messenger_api_integration[each.key].id}"
}

resource "aws_apigatewayv2_deployment" "ws_messenger_api_deployment" {
    for_each  = var.websocket_apis
    api_id    = aws_apigatewayv2_api.ws_messenger_api_gateway[each.key].id
  
    lifecycle {
        create_before_destroy = true
    }

    depends_on = [ aws_apigatewayv2_route.ws_message_api_message_route ]
}

resource "aws_apigatewayv2_stage" "ws_messenger_api_stage" {
    for_each  = var.websocket_apis
    api_id    = aws_apigatewayv2_api.ws_messenger_api_gateway[each.key].id
    name   = "${each.key}-stage"
    auto_deploy = true
    tags = local.tags
}
