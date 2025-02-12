resource "aws_s3_bucket" "buckets" {
  for_each = var.s3_buckets
  bucket_prefix = "${each.value.prefix}-"
  tags = local.tags 
}

locals {
  bucket_names_map = {
    for key, value in var.s3_buckets :
    "s3_${key}" => aws_s3_bucket.buckets[key].id
  }
}

resource "aws_s3_bucket_notification" "aws-lambda-trigger" {
  for_each = var.lambda_s3_notification
  bucket = aws_s3_bucket.buckets[each.value.bucket].id
  dynamic "lambda_function" {
    for_each = each.value.function
    content {
      lambda_function_arn = aws_lambda_function.chatbotenv_lambda[lambda_function.value["arn"]].arn
      events = lambda_function.value["events"]
      filter_prefix = lambda_function.value["filter_prefix"]
      filter_suffix = lambda_function.value["filter_suffix"]
    }
  }
  depends_on = [ aws_lambda_permission.allow_s3_bucket ]
}


