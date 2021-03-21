import boto3
import json
import datetime
from tokened_client import tokened_client_ec2 as ec2_c
from describe_ec2_instances import dateSerializer as dateToJson

#returns jsons of instances and security groups
def ec2_api_details():
    ec2 = boto3.client('ec2')
    
    reponse_sg = ec2.describe_security_groups()
    securityGroups = json.dumps(response_sg, indent=4)
    
    return securityGroups
    