import json

def getSuperInstance(frontend_instances_data, frontend_balancer_data, frontend_rds_data):

    instances = frontend_instances_data["Instances"]
    balancers = frontend_balancer_data["LoadBalancers"]
    databases = frontend_rds_data["Databases"]

    superJson = {"Instances":instances, "LoadBalancers":balancers, "Databases":databases}

    return superJson