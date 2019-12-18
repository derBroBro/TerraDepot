output "settings"{
    value = "Please create a CNAME for ${var.domain} to ${aws_api_gateway_domain_name.main.0.cloudfront_domain_name}"
}

output "instructions"{
    value = "You create can create you first project here https://${var.domain}/project/new"
}
