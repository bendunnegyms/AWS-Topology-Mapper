import boto3
import json
import datetime
from tokened_client import tokened_client_ec2 as ec2_c
from tokened_client import tokened_client_elb as elb_c

#returns jsons of instances and security groups
def ec2_api_details(access_key,secret_key):
    ec2 = ec2_c(access_key, secret_key)
    response_instances = ec2.describe_instances()
    reponse_sg = ec2.describe_security_groups()

    securityGroups = json.dumps(response_sg, indent=4)
    instances = json.dumps(response_instances, default = dateserializer, indent=4)

    return securityGroups, instances
    
#returns jsons of load balancer data
def elb_api_details(access_key,secret_key):
    elb = elb_c(access_key, secret_key)
    response_balancers = elb.describe_load_balancers()

    balancers = json.dumps(balancer_attributes, default = dateserializer, indent=4)

    return balancers

#Used to convert datetime to string for json
def dateSerializer(input):
    if isinstance(input, datetime.datetime):
        return input.__str__()