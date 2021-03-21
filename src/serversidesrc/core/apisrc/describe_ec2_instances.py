import boto3
import json
import datetime
from tokened_client import tokened_client_ec2 as ec2_c

#returns jsons of instances and security groups
def ec2_api_details():
    ec2 = boto3.client('ec2')

    response_instances = ec2.describe_instances()
    instances = json.dumps(response_instances, default = dateserializer, indent=4)

    return instances
    

#Used to convert datetime to string for json
def dateSerializer(input):
    if isinstance(input, datetime.datetime):
        return input.__str__()