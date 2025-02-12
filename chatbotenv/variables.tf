
variable "region" {
    type = string
    default = "us-east-1"
}

variable "env" {
    type = string
}

variable "product_code" {
    type = string
}

variable "cookie_and_token_expiration_time_in_minutes" {
  default = "60"
  type = string
}

variable "user_pool_name" {
  default = "cdn-user-pool"
  type = string
}

variable "chatbotenv_lambda_functions" {
  type = map(object({
    template = string
    route = string
    environment_variables = list(string)
    additional_env_variables = map(string)
    s3_trigger = string
    api_type = string
  }))
  default = {
    "chatbotenv-generate-presigned" = {
      template = "chatbotenv-generate-presigned"
      environment_variables = []
      additional_env_variables = {}
      s3_trigger = null
      route = "presigned"
      api_type = "REST_CORS"
    },
    "chatbotenv-code-review-summary" = {
      template = "chatbotenv-code-review-summary"
      route = "codereview"
      environment_variables = []
      additional_env_variables = {
        "table_doc_status" = "chatbotenv-document-status"
      }
      s3_trigger = null
      api_type = "REST_CORS"
    },
    "chatbotenv-code-analyzer" = {
      template = "chatbotenv-code-analyzer"
      s3_trigger = "code_submission_bucket"
      route = "codeanalyzer"
      api_type = "NONE"
      environment_variables = []
      additional_env_variables    = {
        "model_id" = "amazon.titan-text-premier-v1:0",
        "vector_top_n" = "5",
        "tempreture" = "0.7",
        "topP" = "0.5",
        "maxTokenCount" = "3072",
        "application_id"="LVDV1OOXQ4",
        "chatbotenv_code_profiler_fn_name" = "chatbotenv-code-profiler"
        "table_doc_status" = "chatbotenv-document-status"
      }
    },
    "chatbotenv-code-profiler" = {
      template = "chatbotenv-code-profiler"
      s3_trigger = null
      route = "codeprofiler"
      api_type = "NONE"
      environment_variables = []
      additional_env_variables    = {
        "anthropic_version" = "bedrock-2023-05-31",
        "maxTokenCount" = "8192",
        "model_id" = "anthropic.claude-3-5-sonnet-20240620-v1:0",
        "role" = "user",
        "s3_code_submission_bucket" = "code-analyzer-20240711095206246300000002",
        "table_bedrock_interaction_logs" = "chatbotenv-bedrock_interaction_logs",
        "table_doc_status" = "chatbotenv-document-status",
        "vector_top_n" = "5",
        "tempreture" = "0.7",
        "topP" = "0.5",
        "topK"="250",
        "application_id"="LVDV1OOXQ4"
      }
    }
  }
}

variable "websocket_apis" {
  type = map(object({
    connect_lambda_template = string
    disconnect_lambda_template = string
    message_lambda_template = string
    route = string
    timeout = number
    environment_variables = list(string)
    additional_env_variables = map(string)
  }))
  default = {
    "assistant-chatbot-api" = {
      connect_lambda_template     = "chatbotenv-chatbot-connect"
      disconnect_lambda_template  = "chatbotenv-chatbot-disconnect"
      message_lambda_template     = "chatbotenv-chatbot-message"
      route                       = "sendmessage"
      timeout                     = 900
      environment_variables       = []
      additional_env_variables    = {
        "model_id" = "anthropic.claude-3-5-sonnet-20240620-v1:0",
        "vector_top_n" = "5",
        "tempreture" = "0.7",
        "topP" = "0.5",
        "topK" = "50",
        "maxTokenCount" = "3072"
      }
    }
  }
}

variable "s3_buckets" {
  type = map(object({
    prefix = string
  }))
  default = {
    code_submission_bucket = {
      prefix = "code-analyzer"
    }

  }
}

variable "lambda_s3_notification" {
  type = map(object({
    bucket      = any
    function    = map(object({
      arn                 = string
      events              = list(string)
      filter_prefix       = string
      filter_suffix       = string
    }))
  }))
  default = {
    code_reviewer = {
      bucket = "code_submission_bucket"
      function = {
          code_submission = {
            arn = "chatbotenv-code-analyzer"
            events =  ["s3:ObjectCreated:*"]
            filter_prefix       = ""
            filter_suffix       = ""
          }
      }
    }
  }
}

variable "dynamodb_tables" {
    type = map(object({
        name = string
        billing_mode = string
        hash_key = string
        # range_key = optional(string,null)
        attribute = map(object({
            name = string
            type = string
        }))
    }))
    default = {
        bedrock_interaction_logs = {
            name = "bedrock_interaction_logs"
            billing_mode = "PAY_PER_REQUEST"
            hash_key = "appcode"
            # range_key = "connectionId"
            attribute = {
                sub = {
                    name = "appcode"
                    type = "S"
                }
                # email = {
                #     name = "connectionId"
                #     type = "S"
                # }
            }
        }
    }
}

variable "acm_certificate_arn" {
    type = string
    default = "arn:aws:acm:us-east-1:474668381977:certificate/1108be39-91af-4872-b8bd-563b289d2d42"
}

# variable "lambda_layers" {
#   default = {
#     psycopg2-requests = {
#       compatible_architectures  = ["x86_64"]
#       compatible_runtimes       = ["python3.10"]
#       filename                  = "common_layers/psycopg2-requests-layer.zip"
#     }
#   }
# }