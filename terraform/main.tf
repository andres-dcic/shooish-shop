terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region     = var.aws_region
  access_key = "test"
  secret_key = "test"

  s3_use_path_style = true

  endpoints {
    s3 = var.localstack_s3_endpoint
    sts = "http://localhost:4566"
  }

  skip_credentials_validation = true
  skip_requesting_account_id  = true
}

resource "aws_s3_bucket" "workshop" {
  bucket = var.bucket_name
}



resource "aws_s3_bucket_public_access_block" "workshop" {
  bucket = aws_s3_bucket.workshop.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

