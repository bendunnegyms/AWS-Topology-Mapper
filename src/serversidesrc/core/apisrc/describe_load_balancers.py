import boto3
import json

from .dateSerializer import dateSerializer as dateToJson

#returns jsons of load balancer data
def elb_api_details():
    elb = boto3.client('elb')
    response_balancers = elb.describe_load_balancers()

    return response_balancers