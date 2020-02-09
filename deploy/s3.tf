data "aws_caller_identity" "current" {}

resource "aws_s3_bucket" "state_bucket" {
  bucket = "${data.aws_caller_identity.current.account_id}-${var.name}"
  acl    = "private"

  versioning {
    enabled = true
  }
}

resource "aws_s3_bucket_notification" "trigger_report" {
  bucket = aws_s3_bucket.state_bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.lambda_report.arn
    events              = ["s3:ObjectCreated:*"]
  }
}