import json

def getSuperInstance(frontend_instances_data, frontend_balancer_data, frontend_rds_data, frontend_app_balancer_data):

    instances = frontend_instances_data["Instances"]
    balancers = frontend_balancer_data["LoadBalancers"]
    app_balancers = frontend_app_balancer_data["AppBalancers"]
    databases = frontend_rds_data["Databases"]

    superJson = {"Instances":instances, "LoadBalancers":balancers, "AppBalancers":app_balancers, "Databases":databases}

    return superJson