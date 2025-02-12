resource "aws_iam_role" "chatbotenv_lambda_role" {
  name = "${local.prefix}-lambda-role"
  tags = local.tags
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
        Effect = "Allow",
        Action = [
            "sts:AssumeRole",
        ],
        Principal =  {
          Service: [
            "lambda.amazonaws.com",
            "apigateway.amazonaws.com",
            "s3.amazonaws.com"]
        },
    }]
  })

#   assume_role_policy =<<EOF
#   {
#     "Version": "2012-10-17",
#     "Statement": [
#       {
#         "Action": "sts:AssumeRole",
#         "Principal": {
#           "Service": ["lambda.amazonaws.com",
#                 "apigateway.amazonaws.com",
#                 "s3.amazonaws.com"]
#         },
#         "Effect": "Allow",
#         "Sid": ""
#       }
#     ]
#   }
#   EOF
}

resource "aws_iam_role_policy" "chatbotenv_lambda_role_policy" {
  name = "${local.prefix}-lambda-policy"
  role = "${aws_iam_role.chatbotenv_lambda_role.id}"
  policy =jsonencode({
    Version = "2012-10-17",
    Statement = [{
        Effect = "Allow",
        Action = ["*"],
        Resource = ["*"],
    }]
  })
  # policy =<<EOF
  # {
  #   "Version": "2012-10-17",
  #   "Statement": [
  #     {
  #       "Effect": "Allow",
  #       "Action": "*",
  #       "Resource": "*"
  #     }
  #   ]
  # }
  # EOF
}

data "archive_file" "chatbotenv_lambda_archive" {
    for_each = var.chatbotenv_lambda_functions
    type        = "zip"
    source_dir  = "${path.module}/source/${each.value.template}"
    output_path = "${path.module}/source/archive/${each.value.template}.zip"
}


resource "aws_lambda_function" "chatbotenv_lambda" {
    for_each = var.chatbotenv_lambda_functions
        filename         = data.archive_file.chatbotenv_lambda_archive[each.key].output_path
        source_code_hash = data.archive_file.chatbotenv_lambda_archive[each.key].output_base64sha256
        function_name    = each.key
        role             = aws_iam_role.chatbotenv_lambda_role.arn
        runtime           = "python3.10"
        handler           = "lambda_function.lambda_handler"
        timeout           = 900
        tags              =local.tags
        # layers = [for l in each.value.lambda_layers : aws_lambda_layer_version.lambda_layers[l].arn]
        environment {
            variables = merge(local.common_lambda_environment_vars,
                        each.value.additional_env_variables)
        }
}

resource "aws_lambda_permission" "allow_s3_bucket" {
  for_each = local.lambda_with_s3_trigger
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.chatbotenv_lambda[each.key].function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.buckets[var.chatbotenv_lambda_functions[each.key].s3_trigger].arn
  depends_on = [ aws_lambda_function.chatbotenv_lambda, aws_s3_bucket.buckets]
}


resource "aws_lambda_permission" "lambda_permission" {
  for_each    = local.rest_lambda_functions
	action        = "lambda:InvokeFunction"
	function_name = aws_lambda_function.chatbotenv_lambda[each.key].function_name
	principal     = "apigateway.amazonaws.com"
	source_arn = "${aws_api_gateway_deployment.lambda_rest_deployment.execution_arn}/*/*/*"
  depends_on = [ aws_api_gateway_deployment.lambda_rest_deployment, aws_lambda_function.chatbotenv_lambda, ]
}

# resource "aws_lambda_layer_version" "lambda_layers" {
#   for_each = var.lambda_layers
#   layer_name = "${local.prefix}-${each.key}-layer"
#   filename = "${path.module}/source/${each.value.filename}"
  
# }