
from describe_ec2_instances import ec2_api_details as ec2
from describe_sec_groups import security_group_api_details as secgroups
from describe_rds_instances import getRDSDetails as rds
from describe_load_balancers import elb_api_details as elb

from dateSerializer import dateSerializer as dateToJson

from databases_to_frontend import databases_to_frontend_format as fe_format_rds
from to_frontend_format import ec2_instances_to_frontend_format as fe_format_ec2
from loadbalancers_to_frontend import load_balancers_to_frontend_format as fe_format_elb

from node_data_to_frontend import createNodeData as get_node_data
from all_instances_to_Json import getSuperInstance as fe_format_all_instances

import datetime
import json

sg = secgroups()
ec2 = ec2()
elb = elb()
rds = rds()

instances_data = fe_format_ec2(sg,ec2)
balancers_data = fe_format_elb(sg,elb)
databases_data = fe_format_rds(sg,rds)

all_instances = fe_format_all_instances(instances_data, balancers_data, databases_data)

node_data = get_node_data(all_instances)

with open("./src/serversidesrc/core/apisrc/test.json", "w") as fp:
       json.dump(node_data, fp, indent=4)



'''
rds_response = rds()
rds_formatted = json.dumps(rds_response, default = dateToJson, indent=4)
print(rds_formatted)

with open("./src/serversidesrc/core/apisrc/dbs_instances.json", "w") as fp:
       json.dump(rds_response, fp, default=dateToJson, indent=4)

'''
'''
instances = fe_format_ec2(secgroups(), ec2())
print(json.dumps(instances,indent=4))

'''
'''
with open("./src/serversidesrc/core/apisrc/instances.json", "w") as fp:
       json.dump(instances, fp, default=dateToJson, indent=4)
'''
'''
print(len(instances["Instances"]))
'''