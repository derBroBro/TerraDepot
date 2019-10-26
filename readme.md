# About the project
This project is targeting to provide an easy to use s3 backend for [terraform](https://www.terraform.io/).  
You may complain that there is already a built-in backend for aws s3 which can be used.
And yes - you are right the is something similar but also different as this approach.  

## Problems of the build-in s3 backend
- Some setup effort required
  - IAM users must be created and maintained for each project
  - A Bucket (or complex policy) must be created
  - Can be handled by for example [terragrunt](https://github.com/gruntwork-io/terragrunt) but this is also one further component
- If you want to do it right, you have to handle two AWS credentials which the same time (for tf and the backend)  

## Idea behind this approach
You set up the backend ONCE for your organization. Afterward, everyone can set up the backend in terraform just by adding a unique URL and a self-defined key. If the project is already there the access will just be allowed if you have the right key provided. If the project is new, the set key will be stored and is mandatory for further operations
All data is persisted in one bucket incl. versioning.  

To use it an HTTP endpoint is provided which you can add to your terraform project. 
Behind all data (tfstate and config) is stored in a bucket in a folder named after the project id. 

# Setup
## Deploy the server-side
```
git clone https://github.com/derBroBro/terraform-http-backend.git
cd terraform-http-backend/deploy
terraform apply
```
> You must provide a name for the project. This will be used for the functions, IAM user and the bucket. For this it must be **unique**!

## For each project
Add a file named *backend.tf* with the following content:
```hcl
terraform {
  backend "http" {
    address = "https://YourUrlHere/test/project/YourProjectNameHere?key=YourKeyHere"
  }
}
```
The key should be removed from the repo and be provided elsewhere. 
> The key is setup on the first use. If you want to change it, modify the *config.json* within the bucket.


# Further opportunities
There are a lot of extensions possible for this backend.
Just some ideas:  
- [ ] Trigger a central webhook for each state-change  
- [ ] List and show all states on a central place  

# Todo
- [ ] Setup proper testing
- [ ] Add custom Urls


