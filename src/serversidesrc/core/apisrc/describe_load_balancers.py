import boto3
import json
import datetime
from tokened_client import tokened_client_elb as elb_c
from describe_ec2_instances import dateSerializer as dateToJson

#returns jsons of load balancer data
def elb_api_details(access_key,secret_key):
    elb = elb_c(access_key, secret_key)
    response_balancers = elb.describe_load_balancers()

    balancers = json.dumps(balancer_attributes, default = dateToJson, indent=4)

    return balancers