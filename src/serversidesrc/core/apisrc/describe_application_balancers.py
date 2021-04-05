import boto3
import json

def getAppBalancerDetails():
    elb = boto3.client('elbv2')
    balancer_attributes = elb.describe_load_balancers()


    return balancer_attributes