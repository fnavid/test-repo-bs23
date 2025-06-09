terraform {
  backend "s3" {
    bucket         = "my-terraform-state-fateen"
    key            = "eks/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}

provider "aws" {
  region = "us-east-1"
}

module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  version         = "~> 20.0"

  cluster_name    = "my-eks-cluster"
  cluster_version = "1.29"
  subnet_ids      = module.vpc.private_subnets
  vpc_id          = module.vpc.vpc_id

  enable_irsa = true

  eks_managed_node_groups = {
    default = {
      desired_size = 1
      max_size     = 1
      min_size     = 1

      instance_types = ["t3.micro"]
      capacity_type  = "ON_DEMAND"
    }
  }

  tags = {
    Environment = "dev"
    Project     = "fastapi-app"
  }
}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.1"

  name = "eks-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["us-east-1a", "us-east-1b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]

  enable_nat_gateway = false
  single_nat_gateway = true

  tags = {
    Environment = "dev"
    Project     = "fastapi-weather"
  }
}
