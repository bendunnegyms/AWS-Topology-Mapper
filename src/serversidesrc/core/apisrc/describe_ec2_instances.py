import boto3
import json
import datetime
from tokened_client import tokened_client_ec2 as ec2_c

#returns jsons of instances and security groups
def ec2_api_details(access_key,secret_key):
    ec2 = ec2_c(access_key, secret_key)
    response_instances = ec2.describe_instances()
    reponse_sg = ec2.describe_security_groups()

    #write response_sg to securityGroups file
    with open("securityGroups.json", "w") as fp:
        json.dump(response_sg, fp, indent=4)

    #write response_instances to instances file
    with open("./instances.json", "w") as fp:
        json.dump(response_instances, fp, default = dateS, indent=4)
    

    

#Used to convert datetime to string for json
def dateSerializer(input):
    if isinstance(input, datetime.datetime):
        return input.__str__()