data "aws_availability_zones" "available" {}

/*module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  version = "v5.8.1"
  create_vpc = true

  name = "${local.prefix}-local.product"
  cidr = local.vpc_cidr
  azs  = slice(data.aws_availability_zones.available.names, 0, 3)
  enable_nat_gateway = false
  enable_dns_support = true
  enable_dns_hostnames = true
  
  tags = local.tags
}*/