import boto3

def tokened_client_ec2(access_key, secret_key):
    client = boto3.client(
        'ec2',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )
    return client

def tokened_client_elb(access_key, secret_key):
    client = boto3.client(
        'elb',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )