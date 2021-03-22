import boto3
import json


#returns jsons of instances and security groups
def ec2_api_details():
    ec2 = boto3.client('ec2')
    
    reponse_sg = ec2.describe_security_groups()
    securityGroups = json.dumps(response_sg, indent=4)
    
    return securityGroups
    