import boto3
import json


#returns jsons of instances and security groups
def security_group_api_details():
    ec2 = boto3.client('ec2')
    
    response_sg = ec2.describe_security_groups()
    # securityGroups = json.dumps(response_sg, indent=4)
    # NB - IP Permissions should be added to the database for future access

    return response_sg
    