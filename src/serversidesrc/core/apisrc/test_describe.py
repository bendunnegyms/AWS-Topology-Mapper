from to_frontend_format import ec2_instances_to_frontend_format as fe_format_ec2
from describe_ec2_instances import ec2_api_details as ec2
from describe_sec_groups import security_group_api_details as secgroups
from describe_rds_instances import getRDSDetails as rds
from dateSerializer import dateSerializer as dateToJson
import datetime
import json

'''
rds_response = rds()
rds_formatted = json.dumps(rds_response, default = dateToJson, indent=4)
print(rds_formatted)

with open("./src/serversidesrc/core/apisrc/dbs_instances.json", "w") as fp:
       json.dump(rds_response, fp, default=dateToJson, indent=4)

'''

instances = fe_format_ec2(secgroups(), ec2())
print(json.dumps(instances,indent=4))
'''
with open("./src/serversidesrc/core/apisrc/instances.json", "w") as fp:
       json.dump(instances, fp, default=dateToJson, indent=4)
'''

print(len(instances["Instances"]))

