module "chatbotenv" {
    source      ="./chatbotenv"
    env         = var.environment
    product_code = var.short_name
}