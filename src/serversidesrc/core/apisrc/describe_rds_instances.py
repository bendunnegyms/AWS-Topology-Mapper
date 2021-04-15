import boto3
import json

from .dateSerializer import dateSerializer as dateToJson

def getRDSDetails():
    rds = boto3.client('rds')
    rds_attributes = rds.describe_db_instances()

    
    rdsInstances = json.dumps(rds_attributes, default = dateToJson, indent=4)

    return rds_attributes