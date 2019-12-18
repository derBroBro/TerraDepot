# Lambda
resource "aws_lambda_permission" "apigw_lambda_state" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_state.function_name
  principal     = "apigateway.amazonaws.com"

  # More: http://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-control-access-using-iam-policies-to-invoke-api.html
  # source_arn = "arn:aws:execute-api:${var.region}:${var.accountId}:${aws_api_gateway_rest_api.api.id}/*/${aws_api_gateway_method.method.http_method}${aws_api_gateway_resource.resource.path}"
  source_arn = "${aws_api_gateway_rest_api.api.execution_arn}/*/*/*"
}
resource "aws_lambda_permission" "apigw_lambda_new" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_new.function_name
  principal     = "apigateway.amazonaws.com"

  # More: http://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-control-access-using-iam-policies-to-invoke-api.html
  # source_arn = "arn:aws:execute-api:${var.region}:${var.accountId}:${aws_api_gateway_rest_api.api.id}/*/${aws_api_gateway_method.method.http_method}${aws_api_gateway_resource.resource.path}"
  source_arn = "${aws_api_gateway_rest_api.api.execution_arn}/*/*/*"
}
 
data "archive_file" "deploy_pkg" {
  type        = "zip"
  source_dir  = "${path.module}/../code/"
  output_path = "${path.module}/deploy_pkg.zip"
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
      LOG_LEVEL = "INFO"
    }
  }
}

