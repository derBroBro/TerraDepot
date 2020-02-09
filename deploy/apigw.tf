# API GW

## Rest API
resource "aws_api_gateway_rest_api" "api" {
  name        = var.name
  description = "Proxy to handle requests to our API"
}

## Ressources
resource "aws_api_gateway_resource" "project" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  path_part   = "project"
}
resource "aws_api_gateway_resource" "project_id" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_resource.project.id
  path_part   = "{projectId}"
}
resource "aws_api_gateway_resource" "project_state" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_resource.project_id.id
  path_part   = "terraform.tfstate"
}
resource "aws_api_gateway_resource" "project_info" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_resource.project_id.id
  path_part   = "info"
}
resource "aws_api_gateway_resource" "project_new" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_resource.project.id
  path_part   = "new"
}

## Methodes
resource "aws_api_gateway_method" "method_state" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.project_state.id
  http_method = "ANY"
  request_parameters = {
    "method.request.path.proxy" = true
  }

  authorization = "CUSTOM"
  authorizer_id = aws_api_gateway_authorizer.auth.id
}
resource "aws_api_gateway_method" "method_new" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.project_new.id
  http_method = "ANY"
  request_parameters = {
    "method.request.path.proxy" = true
  }

  authorization = "CUSTOM"
  authorizer_id = aws_api_gateway_authorizer.auth.id
}
resource "aws_api_gateway_method" "method_info" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.project_info.id
  http_method = "ANY"
  request_parameters = {
    "method.request.path.proxy" = true
  }

  authorization = "CUSTOM"
  authorizer_id = aws_api_gateway_authorizer.auth.id
}

## Integration
resource "aws_api_gateway_integration" "integration_state" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.project_state.id
  http_method             = aws_api_gateway_method.method_state.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.lambda_state.invoke_arn
}
resource "aws_api_gateway_integration" "integration_new" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.project_new.id
  http_method             = aws_api_gateway_method.method_new.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.lambda_new.invoke_arn
}
resource "aws_api_gateway_integration" "integration_info" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.project_info.id
  http_method             = aws_api_gateway_method.method_new.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.lambda_info.invoke_arn
}


## Deployment
resource "aws_api_gateway_deployment" "prod" {
  depends_on = [
    "aws_api_gateway_integration.integration_state",
    "aws_api_gateway_integration.integration_info",
    "aws_api_gateway_integration.integration_new",
    "aws_api_gateway_authorizer.auth"
  ]

  rest_api_id = aws_api_gateway_rest_api.api.id
  stage_name  = "prod"
  variables = {
    deployed_at = "${timestamp()}"
  }
  lifecycle {
    create_before_destroy = true
  }
}
resource "aws_api_gateway_base_path_mapping" "prod" {
  api_id      = aws_api_gateway_rest_api.api.id
  stage_name  = aws_api_gateway_deployment.prod.stage_name
  domain_name = aws_api_gateway_domain_name.main.0.domain_name
}

## Custom Domain
resource "aws_api_gateway_domain_name" "main" {
  domain_name     = var.domain
  certificate_arn = var.cert_arn
  count           = (var.domain != "" ? 1 : 0)
}

## Auth
resource "aws_api_gateway_authorizer" "auth" {
  name = "auth"
  type = "REQUEST"
  #identity_source        = "method.request.header.SomeHeaderName"
  rest_api_id                      = "${aws_api_gateway_rest_api.api.id}"
  authorizer_uri                   = "${aws_lambda_function.lambda_auth.invoke_arn}"
  authorizer_credentials           = "${aws_iam_role.auth.arn}"
  authorizer_result_ttl_in_seconds = 0
}
resource "aws_api_gateway_gateway_response" "auth" {
  rest_api_id   = "${aws_api_gateway_rest_api.api.id}"
  status_code   = "401"
  response_type = "UNAUTHORIZED"

  response_templates = {
    "application/json" = "{'message':$context.error.messageString}"
  }

  response_parameters = {
    "gatewayresponse.header.WWW-Authenticate" = "'Basic'"
  }
}
