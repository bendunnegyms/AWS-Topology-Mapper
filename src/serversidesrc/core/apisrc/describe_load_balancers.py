import boto3
import json
import datetime
from describe_ec2_instances import dateSerializer as dateToJson

#returns jsons of load balancer data
def elb_api_details():
    elb = boto3.client('elb')
    response_balancers = elb.describe_load_balancers()

    balancers = json.dumps(balancer_attributes, default = dateToJson, indent=4)

    return balancers