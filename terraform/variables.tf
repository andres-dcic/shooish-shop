variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "localstack_s3_endpoint" {
  type    = string
  default = "http://localhost:4566"
}

variable "bucket_name" {
  type    = string
  default = "shoosh-workshop"
}
