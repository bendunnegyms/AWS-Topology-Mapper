import json

#gets the security group name, from corresponding id
def get_sg_name(sg_id, sg_data_list):
    
    for entry in sg_data_list:
        entry_sg_id = entry["GroupId"]
        if(entry_sg_id == sg_id):
            return entry["GroupName"]

