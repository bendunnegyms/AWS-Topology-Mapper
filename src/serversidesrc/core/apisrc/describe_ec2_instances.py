import boto3
import json

from dateSerializer import dateSerializer as dateToJson

#returns jsons of instances and security groups
def ec2_api_details():
    ec2 = boto3.client('ec2')

    response_instances = ec2.describe_instances()
    instances = json.dumps(response_instances, default = dateToJson, indent=4)

    return instances
    

