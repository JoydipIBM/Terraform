resource "aws_dynamodb_table" "chatbotenv_dynamo" {
    for_each = var.dynamodb_tables
    name = "${local.prefix}-${each.value.name}"
    billing_mode = each.value.billing_mode
    hash_key = each.value.hash_key
    #range_key = each.value.range_key
    dynamic "attribute" {
        for_each = each.value.attribute
        content {
            name = attribute.value.name
            type = attribute.value.type
        }
    }
    tags = local.tags
}


locals {
  table_names_map = {
    for key, value in var.dynamodb_tables :
    "table_${key}" => aws_dynamodb_table.chatbotenv_dynamo[key].id
  }
}
