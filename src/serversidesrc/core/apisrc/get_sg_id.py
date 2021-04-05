def get_sg_id(sg_name, sg_data_list):
    
    for entry in sg_data_list:
        entry_sg_name = entry["GroupName"]
        if(entry_sg_name == sg_name):
            return entry["GroupId"]
