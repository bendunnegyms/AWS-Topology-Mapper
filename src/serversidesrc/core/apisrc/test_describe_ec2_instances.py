from to_frontend_format import ec2_instances_to_frontend_format
from describe_ec2_instances import ec2_api_details as ec2
from describe_sec_groups import security_group_api_details as secgroups
import json

print(json.dumps(ec2_instances_to_frontend_format(secgroups(),ec2()), indent = 4))