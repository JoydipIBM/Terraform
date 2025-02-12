resource "aws_api_gateway_rest_api" "chatbotenv_rest_api" {
	name = "${local.prefix}-rest-api"
	description = ""
	tags = local.tags
	endpoint_configuration {
		types = ["REGIONAL"]
	}
}

resource "aws_api_gateway_resource" "chatbotenv_rest_resource" {
    for_each          = local.rest_lambda_functions
    rest_api_id       = aws_api_gateway_rest_api.chatbotenv_rest_api.id
    parent_id         = aws_api_gateway_rest_api.chatbotenv_rest_api.root_resource_id
    path_part         = var.chatbotenv_lambda_functions[each.key].route == null ? each.key : var.chatbotenv_lambda_functions[each.key].route

}

resource "aws_api_gateway_method" "chatbotenv_rest_methods" {
    for_each      = local.rest_lambda_functions
    authorization = "NONE"
    http_method   = "POST"
    resource_id   = aws_api_gateway_resource.chatbotenv_rest_resource[each.key].id
    rest_api_id   = aws_api_gateway_rest_api.chatbotenv_rest_api.id
}

resource "aws_api_gateway_integration" "chatbotenv_rest_integration" {
    for_each      = local.rest_lambda_functions
    http_method = aws_api_gateway_method.chatbotenv_rest_methods[each.key].http_method
    resource_id = aws_api_gateway_resource.chatbotenv_rest_resource[each.key].id
    rest_api_id = aws_api_gateway_rest_api.chatbotenv_rest_api.id
    integration_http_method = "POST"
    type        = "AWS_PROXY"
    uri         = aws_lambda_function.chatbotenv_lambda[each.key].invoke_arn
    #credentials = aws_iam_role.chatbotenv_lambda_role.arn
    credentials = aws_iam_role.chatbotenv_lambda_role.arn
}




# ========================= REST CORS APIs ===========================================

resource "aws_api_gateway_resource" "cors_resource" {
	for_each      = local.rest_cors_lambda_functions
    path_part     = var.chatbotenv_lambda_functions[each.key].route == null ? each.key : var.chatbotenv_lambda_functions[each.key].route
    parent_id     = aws_api_gateway_rest_api.chatbotenv_rest_api.root_resource_id
    rest_api_id   = aws_api_gateway_rest_api.chatbotenv_rest_api.id
}

resource "aws_api_gateway_method" "cors_options_method" {
	for_each      = local.rest_cors_lambda_functions
    rest_api_id   = aws_api_gateway_rest_api.chatbotenv_rest_api.id
    resource_id   = aws_api_gateway_resource.cors_resource[each.key].id
    http_method   = "OPTIONS"
    authorization = "NONE"
}

resource "aws_api_gateway_method_response" "cors_options_200" {
	for_each      = local.rest_cors_lambda_functions
    rest_api_id   = aws_api_gateway_rest_api.chatbotenv_rest_api.id
    resource_id   = aws_api_gateway_resource.cors_resource[each.key].id
    http_method   = aws_api_gateway_method.cors_options_method[each.key].http_method
    status_code   = "200"
    response_models = {
        "application/json" = "Empty"
    }
    response_parameters = {
        "method.response.header.Access-Control-Allow-Credentials" = false,
        "method.response.header.Access-Control-Allow-Headers" = false,
        "method.response.header.Access-Control-Allow-Methods" = false,
        "method.response.header.Access-Control-Allow-Origin" = false
    }
    depends_on = [aws_api_gateway_method.cors_options_method]
}

resource "aws_api_gateway_integration" "options_integration" {
	for_each      = local.rest_cors_lambda_functions
    rest_api_id   = aws_api_gateway_rest_api.chatbotenv_rest_api.id
    resource_id   = aws_api_gateway_resource.cors_resource[each.key].id
    http_method   = aws_api_gateway_method.cors_options_method[each.key].http_method
    type          = "MOCK"
    depends_on = [aws_api_gateway_method.cors_options_method]
}

resource "aws_api_gateway_integration_response" "options_integration_response" {
	for_each      = local.rest_cors_lambda_functions
    rest_api_id   = aws_api_gateway_rest_api.chatbotenv_rest_api.id
    resource_id   = aws_api_gateway_resource.cors_resource[each.key].id
    http_method   = aws_api_gateway_method.cors_options_method[each.key].http_method
    status_code   = aws_api_gateway_method_response.cors_options_200[each.key].status_code
    response_parameters = {
        "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
        "method.response.header.Access-Control-Allow-Methods" = "'OPTIONS,POST'",
        "method.response.header.Access-Control-Allow-Origin" = "'*'"
    }
    depends_on = [aws_api_gateway_method_response.cors_options_200]
}


resource "aws_api_gateway_method" "cors_method" {
	for_each      = local.rest_cors_lambda_functions
    rest_api_id   = aws_api_gateway_rest_api.chatbotenv_rest_api.id
    resource_id   = aws_api_gateway_resource.cors_resource[each.key].id
    http_method   = "POST"
    authorization = "NONE"
}

resource "aws_api_gateway_method_response" "cors_method_response_200" {
	for_each      = local.rest_cors_lambda_functions
    rest_api_id   = aws_api_gateway_rest_api.chatbotenv_rest_api.id
    resource_id   = aws_api_gateway_resource.cors_resource[each.key].id
    http_method   = aws_api_gateway_method.cors_method[each.key].http_method
    status_code   = "200"
    response_parameters = {
        "method.response.header.Access-Control-Allow-Origin" = false
    }
    depends_on = [aws_api_gateway_method.cors_method]
}

resource "aws_api_gateway_integration" "integration" {
	for_each      = local.rest_cors_lambda_functions
    rest_api_id   = aws_api_gateway_rest_api.chatbotenv_rest_api.id
    resource_id   = aws_api_gateway_resource.cors_resource[each.key].id
    http_method   = aws_api_gateway_method.cors_method[each.key].http_method
	integration_http_method = "POST"
    type          = "AWS_PROXY"
	uri           = aws_lambda_function.chatbotenv_lambda[each.key].invoke_arn
	credentials   = aws_iam_role.chatbotenv_lambda_role.arn
    depends_on    = [aws_api_gateway_method.cors_method, aws_lambda_function.chatbotenv_lambda]
}

# ========================= REST CORS APIs ===========================================

resource "aws_api_gateway_deployment" "lambda_rest_deployment" {
	rest_api_id = aws_api_gateway_rest_api.chatbotenv_rest_api.id
	description = "API deployment created by Terraform"

	lifecycle {
		create_before_destroy = true
	}

	depends_on = [
		aws_api_gateway_method.chatbotenv_rest_methods,
		aws_api_gateway_integration.chatbotenv_rest_integration
	]
}

resource "aws_api_gateway_stage" "lambda_rest_stage" {
	deployment_id = aws_api_gateway_deployment.lambda_rest_deployment.id
	rest_api_id   = aws_api_gateway_rest_api.chatbotenv_rest_api.id
	stage_name    = "dev"
	tags = local.tags
	description = ""
}

