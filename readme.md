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
Ex: 
  viewer_certificate {
    cloudfront_default_certificate = true
    #acm_certificate_arn = "arn:aws:acm:us-east-1:685363273140:certificate/5e63d56d-ca5e-458f-a9e0-c19510286dcc"
    acm_certificate_arn = var.acm_certificate_arn
    ssl_support_method = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }
