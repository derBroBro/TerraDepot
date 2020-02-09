# Lambda

## Permission
resource "aws_lambda_permission" "apigw_lambda_auth" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_auth.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_api_gateway_rest_api.api.execution_arn}/*/*/*"
}
resource "aws_lambda_permission" "apigw_lambda_state" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_state.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_api_gateway_rest_api.api.execution_arn}/*/*/*"
}
resource "aws_lambda_permission" "apigw_lambda_new" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_new.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_api_gateway_rest_api.api.execution_arn}/*/*/*"
}
resource "aws_lambda_permission" "apigw_lambda_info" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_info.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_api_gateway_rest_api.api.execution_arn}/*/*/*"
}
resource "aws_lambda_permission" "s3_lambda_report" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_report.function_name
  principal     = "s3.amazonaws.com"

  source_arn = aws_s3_bucket.state_bucket.arn
}

## zip 
resource "null_resource" "pip_install" {
  # Changes to any instance of the cluster requires re-provisioning
  triggers = {
    md52 = "${filemd5("../code/requirements.txt")}"
  }

  provisioner "local-exec" {
    # Bootstrap script called with private_ip of each node in the clutser
    command = "pip install --target ../code/ -r ../code/requirements.txt"
  }
}

data "archive_file" "deploy_pkg" {
  type        = "zip"
  source_dir  = "${path.module}/../code/"
  output_path = "${path.module}/deploy_pkg.zip"
  depends_on  = [
    "null_resource.pip_install"
  ]
}

## function
resource "aws_lambda_function" "lambda_auth" {
  filename      = "deploy_pkg.zip"
  function_name = "${var.name}_auth"
  role          = aws_iam_role.lambda_exec.arn
  handler       = "auth.lambda_handler"
  runtime       = "python3.6"
  source_code_hash = data.archive_file.deploy_pkg.output_base64sha256

  environment {
    variables = {
      S3_BUCKET = aws_s3_bucket.state_bucket.id
      DOMAIN    = var.domain
      KEY       = var.auth_key
      LOG_LEVEL = "INFO"
    }
  }
}
resource "aws_lambda_function" "lambda_state" {
  filename      = "deploy_pkg.zip"
  function_name = "${var.name}_state"
  role          = aws_iam_role.lambda_exec.arn
  handler       = "state.lambda_handler"
  runtime       = "python3.6"
  source_code_hash = data.archive_file.deploy_pkg.output_base64sha256

  environment {
    variables = {
      S3_BUCKET = aws_s3_bucket.state_bucket.id
      DOMAIN    = var.domain
      LOG_LEVEL = "INFO"
    }
  }
}
resource "aws_lambda_function" "lambda_new" {
  filename      = "deploy_pkg.zip"
  function_name = "${var.name}_new"
  role          = aws_iam_role.lambda_exec.arn
  handler       = "new.lambda_handler"
  runtime       = "python3.6"
  source_code_hash = data.archive_file.deploy_pkg.output_base64sha256

  environment {
    variables = {
      S3_BUCKET = aws_s3_bucket.state_bucket.id
      DOMAIN    = var.domain
      KEY       = var.auth_key
      LOG_LEVEL = "INFO"
    }
  }
}
resource "aws_lambda_function" "lambda_info" {
  filename      = "deploy_pkg.zip"
  function_name = "${var.name}_info"
  role          = aws_iam_role.lambda_exec.arn
  handler       = "info.lambda_handler"
  runtime       = "python3.6"
  source_code_hash = data.archive_file.deploy_pkg.output_base64sha256

  environment {
    variables = {
      S3_BUCKET = aws_s3_bucket.state_bucket.id
      DOMAIN    = var.domain
      LOG_LEVEL = "INFO"
    }
  }
}
resource "aws_lambda_function" "lambda_report" {
  filename      = "deploy_pkg.zip"
  function_name = "${var.name}_report"
  role          = aws_iam_role.lambda_exec.arn
  handler       = "report.lambda_handler"
  runtime       = "python3.6"
  source_code_hash = data.archive_file.deploy_pkg.output_base64sha256

  environment {
    variables = {
      S3_BUCKET = aws_s3_bucket.state_bucket.id
      DOMAIN    = var.domain
      LOG_LEVEL = "INFO"
      STATE_TOPIC = aws_sns_topic.state_updates.arn
      CONFIG_TOPIC = aws_sns_topic.config_updates.arn
    }
  }
}