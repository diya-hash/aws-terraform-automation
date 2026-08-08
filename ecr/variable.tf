variable "aws_region" {
  description = "AWS region where the ECR resource will be created"
  type        = string
  default     = "us-east-1"
}
variable "repository_name" {
  description = "Name of the ECR repository"
  type        = string
}
