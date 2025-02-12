resource random_string this {
    length = 10
    special = false
}

# S3 bucket for hosting static website
resource "aws_s3_bucket" "website" {
  bucket = "${local.prefix}-website-${lower(random_string.this.id)}"
  tags = local.tags 
}

resource "aws_s3_bucket_policy" "allow_access_from_cloudfront" {
  bucket = aws_s3_bucket.website.id
  policy = data.aws_iam_policy_document.website_policy_doc.json
}

data "aws_iam_policy_document" "website_policy_doc" {
  statement {
    
    actions = [
      "s3:GetObject",
    ]

    resources = [
      "${aws_s3_bucket.website.arn}/*",
    ]

    condition {
      test     = "StringEquals"
      variable = "aws:SourceArn"
      values   = [aws_cloudfront_distribution.s3_distribution.arn]
    }

    principals {
      type        = "Service"
      identifiers = ["cloudfront.amazonaws.com"]
    }
  }
}

# S3 bucket for cloudfront logs
resource "aws_s3_bucket" "cf_logs" {
  bucket = "${local.prefix}-cf-logs-${lower(random_string.this.id)}"
  tags = local.tags 
}

resource "aws_s3_bucket_policy" "allow_logs_access_from_cloudfront" {
  bucket = aws_s3_bucket.cf_logs.id
  policy = data.aws_iam_policy_document.logs_policy_doc.json
}

data "aws_iam_policy_document" "logs_policy_doc" {
  statement {
    actions = [
      "s3:GetObject",
      "s3:PutObject",
    ]

    resources = [
      "${aws_s3_bucket.cf_logs.arn}/*",
    ]

    principals {
      type        = "Service"
      identifiers = ["cloudfront.amazonaws.com"]
    }
  }
}

resource "aws_s3_bucket_ownership_controls" "log_acl" {
  bucket = aws_s3_bucket.cf_logs.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}


resource "aws_cloudfront_origin_access_control" "default_s3_oac" {
  name                              = "${local.prefix}-s3_oac"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

resource "aws_cloudfront_distribution" "s3_distribution" {
  origin {
    domain_name              = aws_s3_bucket.website.bucket_regional_domain_name
    origin_access_control_id = aws_cloudfront_origin_access_control.default_s3_oac.id
    origin_id                = local.s3_origin_id
  }
  
  
  #data.terraform_remote_state.app-baseline.outputs.region

  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = "index.html"

  logging_config {
    include_cookies = false
    bucket          = aws_s3_bucket.cf_logs.bucket_domain_name
    prefix          = "cloudfront/"
  }

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = local.s3_origin_id

    forwarded_values {
      query_string = true
      headers      = ["Origin"]

      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
  }

  price_class = "PriceClass_200"

  restrictions {
    geo_restriction {
      restriction_type = "none"
#      locations        = ["IN"]
    }
  }

  tags = local.tags
  #aliases = ["*.sandbox.aws.democentral.in"]
  viewer_certificate {
    cloudfront_default_certificate = true
    #acm_certificate_arn = "arn:aws:acm:us-east-1:685363273140:certificate/5e63d56d-ca5e-458f-a9e0-c19510286dcc"
    acm_certificate_arn = var.acm_certificate_arn
    ssl_support_method = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }
}
