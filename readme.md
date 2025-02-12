terraform state list
--------------------------------------------
module.chatbotenv.data.archive_file.chatbotenv_lambda_archive["chatbotenv-code-analyzer"]
module.chatbotenv.data.archive_file.chatbotenv_lambda_archive["chatbotenv-code-profiler"]
module.chatbotenv.data.archive_file.chatbotenv_lambda_archive["chatbotenv-code-review-summary"]
module.chatbotenv.data.archive_file.chatbotenv_lambda_archive["chatbotenv-generate-presigned"]
module.chatbotenv.data.archive_file.ws_connect_lambda_archive["assistant-chatbot-api"]
module.chatbotenv.data.archive_file.ws_disconnect_lambda_archive["assistant-chatbot-api"]
module.chatbotenv.data.archive_file.ws_message_lambda_archive["assistant-chatbot-api"]
module.chatbotenv.data.aws_availability_zones.available
module.chatbotenv.data.aws_iam_policy_document.aibot_logs_policy_doc
module.chatbotenv.data.aws_iam_policy_document.aibot_website_policy_doc
module.chatbotenv.data.aws_iam_policy_document.logs_policy_doc
module.chatbotenv.data.aws_iam_policy_document.website_policy_doc
module.chatbotenv.aws_api_gateway_deployment.lambda_rest_deployment
module.chatbotenv.aws_api_gateway_integration.integration["chatbotenv-code-review-summary"]
module.chatbotenv.aws_api_gateway_integration.integration["chatbotenv-generate-presigned"]
module.chatbotenv.aws_api_gateway_integration.options_integration["chatbotenv-code-review-summary"]
module.chatbotenv.aws_api_gateway_integration.options_integration["chatbotenv-generate-presigned"]
module.chatbotenv.aws_api_gateway_integration_response.options_integration_response["chatbotenv-code-review-summary"]
module.chatbotenv.aws_api_gateway_integration_response.options_integration_response["chatbotenv-generate-presigned"]
module.chatbotenv.aws_api_gateway_method.cors_method["chatbotenv-code-review-summary"]
module.chatbotenv.aws_api_gateway_method.cors_method["chatbotenv-generate-presigned"]
module.chatbotenv.aws_api_gateway_method.cors_options_method["chatbotenv-code-review-summary"]
module.chatbotenv.aws_api_gateway_method.cors_options_method["chatbotenv-generate-presigned"]
module.chatbotenv.aws_api_gateway_method_response.cors_method_response_200["chatbotenv-code-review-summary"]    
module.chatbotenv.aws_api_gateway_method_response.cors_method_response_200["chatbotenv-generate-presigned"]     
module.chatbotenv.aws_api_gateway_method_response.cors_options_200["chatbotenv-code-review-summary"]
module.chatbotenv.aws_api_gateway_method_response.cors_options_200["chatbotenv-generate-presigned"]
module.chatbotenv.aws_api_gateway_resource.cors_resource["chatbotenv-code-review-summary"]
module.chatbotenv.aws_api_gateway_resource.cors_resource["chatbotenv-generate-presigned"]
module.chatbotenv.aws_api_gateway_rest_api.chatbotenv_rest_api
module.chatbotenv.aws_api_gateway_stage.lambda_rest_stage
module.chatbotenv.aws_apigatewayv2_api.ws_messenger_api_gateway["assistant-chatbot-api"]
module.chatbotenv.aws_apigatewayv2_deployment.ws_messenger_api_deployment["assistant-chatbot-api"]
module.chatbotenv.aws_apigatewayv2_integration.ws_connect_api_integration["assistant-chatbot-api"]
module.chatbotenv.aws_apigatewayv2_integration.ws_disconnect_api_integration["assistant-chatbot-api"]
module.chatbotenv.aws_apigatewayv2_integration.ws_messenger_api_integration["assistant-chatbot-api"]
module.chatbotenv.aws_apigatewayv2_integration_response.ws_connect_api_integration_response["assistant-chatbot-api"]
module.chatbotenv.aws_apigatewayv2_integration_response.ws_disconnect_api_integration_response["assistant-chatbot-api"]
module.chatbotenv.aws_apigatewayv2_integration_response.ws_messenger_api_integration_response["assistant-chatbot-api"]
module.chatbotenv.aws_apigatewayv2_route.ws_message_api_message_route["assistant-chatbot-api"]
module.chatbotenv.aws_apigatewayv2_route.ws_messenger_api_connect_route["assistant-chatbot-api"]
module.chatbotenv.aws_apigatewayv2_route.ws_messenger_api_default_route["assistant-chatbot-api"]
module.chatbotenv.aws_apigatewayv2_route.ws_messenger_api_disconnect_route["assistant-chatbot-api"]
module.chatbotenv.aws_apigatewayv2_stage.ws_messenger_api_stage["assistant-chatbot-api"]
module.chatbotenv.aws_cloudfront_distribution.aibot_s3_aibot_distribution
module.chatbotenv.aws_cloudfront_distribution.s3_distribution
module.chatbotenv.aws_cloudfront_origin_access_control.aibot_default_s3_oac
module.chatbotenv.aws_cloudfront_origin_access_control.default_s3_oac
module.chatbotenv.aws_cloudwatch_log_group.chabot_log_group
module.chatbotenv.aws_dynamodb_table.chatbotenv_dynamo["bedrock_interaction_logs"]
module.chatbotenv.aws_iam_role.chatbotenv_lambda_role
module.chatbotenv.aws_iam_role_policy.chatbotenv_lambda_role_policy
module.chatbotenv.aws_lambda_function.chatbotenv_lambda["chatbotenv-code-analyzer"]
module.chatbotenv.aws_lambda_function.chatbotenv_lambda["chatbotenv-code-profiler"]
module.chatbotenv.aws_lambda_function.chatbotenv_lambda["chatbotenv-code-review-summary"]
module.chatbotenv.aws_lambda_function.chatbotenv_lambda["chatbotenv-generate-presigned"]
module.chatbotenv.aws_lambda_function.ws_connect_lambda["assistant-chatbot-api"]
module.chatbotenv.aws_lambda_function.ws_disconnect_lambda["assistant-chatbot-api"]
module.chatbotenv.aws_lambda_function.ws_message_lambda["assistant-chatbot-api"]
module.chatbotenv.aws_lambda_permission.allow_s3_bucket["chatbotenv-code-analyzer"]
module.chatbotenv.aws_s3_bucket.aibot_cf_logs
module.chatbotenv.aws_s3_bucket.aibot_website
module.chatbotenv.aws_s3_bucket.buckets["code_submission_bucket"]
module.chatbotenv.aws_s3_bucket.cf_logs
module.chatbotenv.aws_s3_bucket.website
module.chatbotenv.aws_s3_bucket_notification.aws-lambda-trigger["code_reviewer"]
module.chatbotenv.aws_s3_bucket_ownership_controls.aibot_log_acl
module.chatbotenv.aws_s3_bucket_ownership_controls.log_acl
module.chatbotenv.aws_s3_bucket_policy.aibot_allow_access_from_cloudfront
module.chatbotenv.aws_s3_bucket_policy.aibot_allow_logs_access_from_cloudfront
module.chatbotenv.aws_s3_bucket_policy.allow_access_from_cloudfront
module.chatbotenv.aws_s3_bucket_policy.allow_logs_access_from_cloudfront
module.chatbotenv.random_string.this



Terraform will perform the following actions:

  # module.chatbotenv.data.aws_iam_policy_document.aibot_website_policy_doc will be read during apply
  # (depends on a resource or a module with changes pending)
 <= data "aws_iam_policy_document" "aibot_website_policy_doc" {
      + id            = (known after apply)
      + json          = (known after apply)
      + minified_json = (known after apply)

      + statement {
          + actions   = [
              + "s3:GetObject",
            ]
          + resources = [
              + "arn:aws:s3:::chatbotenv-bot-website-fv6vh6jbqw/*",
            ]

          + condition {
              + test     = "StringEquals"
              + values   = [
                  + "arn:aws:cloudfront::474668381977:distribution/E22SZNM5MB1SER",
                ]
              + variable = "aws:SourceArn"
            }

          + principals {
              + identifiers = [
                  + "cloudfront.amazonaws.com",
                ]
              + type        = "Service"
            }
        }
    }

  # module.chatbotenv.data.aws_iam_policy_document.website_policy_doc will be read during apply
  # (depends on a resource or a module with changes pending)
 <= data "aws_iam_policy_document" "website_policy_doc" {
      + id            = (known after apply)
      + json          = (known after apply)
      + minified_json = (known after apply)

      + statement {
          + actions   = [
              + "s3:GetObject",
            ]
          + resources = [
              + "arn:aws:s3:::chatbotenv-website-fv6vh6jbqw/*",
            ]

          + condition {
              + test     = "StringEquals"
              + values   = [
                  + "arn:aws:cloudfront::474668381977:distribution/E27H6TY9I69APO",
                ]
              + variable = "aws:SourceArn"
            }

          + principals {
              + identifiers = [
                  + "cloudfront.amazonaws.com",
                ]
              + type        = "Service"
            }
        }
    }

  # module.chatbotenv.aws_cloudfront_distribution.aibot_s3_aibot_distribution will be updated in-place
  ~ resource "aws_cloudfront_distribution" "aibot_s3_aibot_distribution" {
      ~ aliases                         = [
          - "*.sandbox.aws.democentral.in",
        ]
        id                              = "E22SZNM5MB1SER"
        tags                            = {
            "Environment" = "dev"
            "ProductCode" = "terraform"
            "managed-by"  = "terraform"
            "region"      = "us-east-1"
        }
        # (21 unchanged attributes hidden)

      ~ viewer_certificate {
          ~ cloudfront_default_certificate = false -> true
            # (4 unchanged attributes hidden)
        }

        # (4 unchanged blocks hidden)
    }

  # module.chatbotenv.aws_cloudfront_distribution.s3_distribution will be updated in-place
  ~ resource "aws_cloudfront_distribution" "s3_distribution" {
        id                              = "E27H6TY9I69APO"
        tags                            = {
            "Environment" = "dev"
            "ProductCode" = "terraform"
            "managed-by"  = "terraform"
            "region"      = "us-east-1"
        }
        # (22 unchanged attributes hidden)

      ~ viewer_certificate {
          ~ cloudfront_default_certificate = false -> true
            # (4 unchanged attributes hidden)
        }

        # (4 unchanged blocks hidden)
    }

  # module.chatbotenv.aws_s3_bucket_policy.aibot_allow_access_from_cloudfront will be updated in-place
  ~ resource "aws_s3_bucket_policy" "aibot_allow_access_from_cloudfront" {
        id     = "chatbotenv-bot-website-fv6vh6jbqw"
      ~ policy = jsonencode(
            {
              - Statement = [
                  - {
                      - Action    = "s3:GetObject"
                      - Condition = {
                          - StringEquals = {
                              - "aws:SourceArn" = "arn:aws:cloudfront::474668381977:distribution/E22SZNM5MB1SER"
                            }
                        }
                      - Effect    = "Allow"
                      - Principal = {
                          - Service = "cloudfront.amazonaws.com"
                        }
                      - Resource  = "arn:aws:s3:::chatbotenv-bot-website-fv6vh6jbqw/*"
                    },
                ]
              - Version   = "2012-10-17"
            }
        ) -> (known after apply)
        # (1 unchanged attribute hidden)
    }

  # module.chatbotenv.aws_s3_bucket_policy.allow_access_from_cloudfront will be updated in-place
  ~ resource "aws_s3_bucket_policy" "allow_access_from_cloudfront" {
        id     = "chatbotenv-website-fv6vh6jbqw"
      ~ policy = jsonencode(
            {
              - Statement = [
                  - {
                      - Action    = "s3:GetObject"
                      - Condition = {
                          - StringEquals = {
                              - "aws:SourceArn" = "arn:aws:cloudfront::474668381977:distribution/E27H6TY9I69APO"
                            }
                        }
                      - Effect    = "Allow"
                      - Principal = {
                          - Service = "cloudfront.amazonaws.com"
                        }
                      - Resource  = "arn:aws:s3:::chatbotenv-website-fv6vh6jbqw/*"
                    },
                ]
              - Version   = "2012-10-17"
            }
        ) -> (known after apply)
        # (1 unchanged attribute hidden)
    }


Plan: 0 to add, 4 to change, 0 to destroy.


Changed acm_certificate_arn value to a variable called viewer_certificate for viewer_certificate section
----------------------------------------------------------------------------------------------------------
Ex: 
  viewer_certificate {
    cloudfront_default_certificate = true
    #acm_certificate_arn = "arn:aws:acm:us-east-1:685363273140:certificate/5e63d56d-ca5e-458f-a9e0-c19510286dcc"
    acm_certificate_arn = var.acm_certificate_arn
    ssl_support_method = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }
