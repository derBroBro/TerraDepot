# About the project
This project is targeting to provide an easy to use s3 backend for terraform.  
You may complain that there is already a built-in backend for aws s3 which can be used.
And yes - you are right the is something similar but also different as this approach.  

## Problems of the build-in s3 backend
- Some setup effort required
  - IAM users must be created and maintained for each project
  - A Bucket (or complex policy) must be created
  - Can be handled by for example terragrunt but this is also one further component
- If you want to do it right, you have to handle two AWS credentials which the same time (for tf and and the backend)  

## Idea behind this approach
You set up the backend ONCE for your organisation. Afterward, everyone can setup the backend in terraform just by adding a uniqe url and a self defined key. If the project is already there the access will just be allowed if you hae the right key provided. If the project is new, the set key will be stored and is mandatory for further operations
All data is persisted in one bucket incl. versioning.  

# Further opportunities
There are a lot of extensions possible for this backend. Just some ideas:  
[ ] Trigger a central webhook for each state-change  
[ ] List and show all states on a central place  

# Todo
[ ] Setup proper testing
