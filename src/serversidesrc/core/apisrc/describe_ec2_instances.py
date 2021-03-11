import boto3
from tokened_client import tokened_client_ec2 as ec2_c

def ec2_api_details(access_key,secret_key):
    ec2 = ec2_c(access_key, secret_key)
    response_instances = ec2.describe_instances()
    reponse_sg = ec2.describe_security_groups()
    print(reponse_sg)