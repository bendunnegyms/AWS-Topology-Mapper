
from .describe_ec2_instances import ec2_api_details as ec2
from .describe_sec_groups import security_group_api_details as secgroups
from .describe_rds_instances import getRDSDetails as rds
from .describe_load_balancers import elb_api_details as elb
from .describe_application_balancers import getAppBalancerDetails as elbv2

from .dateSerializer import dateSerializer as dateToJson

from .databases_to_frontend import databases_to_frontend_format as fe_format_rds
from .to_frontend_format import ec2_instances_to_frontend_format as fe_format_ec2
from .loadbalancers_to_frontend import load_balancers_to_frontend_format as fe_format_elb
from .applicationBalancers_to_frontend import app_balancers_to_frontend_format as fe_format_elbv2

from .node_data_to_frontend import createNodeData as get_node_data
from .all_instances_to_Json import getSuperInstance as fe_format_all_instances

import datetime
import json

def compile_data():
    sg = secgroups()
    ec2_data = ec2()
    elb_data = elb()
    elbv2_data = elbv2()
    rds_data = rds()

    instances_data = fe_format_ec2(sg,ec2_data)
    balancers_data = fe_format_elb(sg,elb_data)
    databases_data = fe_format_rds(sg,rds_data)
    app_balancer_data = fe_format_elbv2(sg, elbv2_data)

    all_instances = fe_format_all_instances(instances_data, balancers_data, databases_data, app_balancer_data)
    node_data = get_node_data(all_instances)
    return node_data
