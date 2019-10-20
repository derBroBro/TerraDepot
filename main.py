from flask import Flask, request
import pprint
import logging
import os
import boto3
import botocore

BUCKET = "malte-terraform"
s3_client = boto3.resource('s3')


app = Flask(__name__)

@app.route('/project/<project_id>', methods = ['POST', 'GET'])
def handle_state(project_id):
    app.logger.info(f"Got request for project {project_id}")
    filename = f"{project_id}.tfstate"
    s3_obj = s3_client.Object(BUCKET, filename)
    if request.method == 'POST':
        data = request.data.decode("utf-8")
        app.logger.debug(data)
        s3_obj.put(Body=data)
        #with open(filename, "w") as file:
        #    file.write(data )
        return data
    if request.method == 'GET':
        # load default file
        try:
            data = s3_obj.get()["Body"].read()
            return data
        # if object does not exists
        except botocore.exceptions.ClientError as e:
            with open(".terraform/terraform.tfstate", "r") as file:
                return file.read()
if __name__ == '__main__':
    app.logger.setLevel(logging.INFO)
    app.run(debug=True)