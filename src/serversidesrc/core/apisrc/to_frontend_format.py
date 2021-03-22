import json

def ec2_instances_to_frontend_format(security_groups_data, instances_data):

    sg_data_list = security_groups_data["SecurityGroups"]

    instance_data = []
    data = instances_data["Reservations"]

    for entry in data:
        instances = entry["Instances"] #- gives list
        for instance in instances:
            instance_id = instance["InstanceId"]
            instance_name = instance["KeyName"]
            instance_IP = instance["PrivateIpAddress"]
            instance_sgs = instance["SecurityGroups"]
            
            instance_outbound = []
            instance_inbound = []

            for sg in instance_sgs:
                sg_id = sg["GroupId"]
                for security_group in sg_data_list:
                    if sg_id == security_group["GroupId"]:
                        #print(json.dumps(security_group, indent=4))
                        for inbound_permission in security_group["IpPermissions"]:
                            protocol = inbound_permission["IpProtocol"]
                            from_port = "-1"
                            to_port = "-1"
                            if protocol != "-1":
                                from_port = inbound_permission["FromPort"]
                                to_port = inbound_permission["ToPort"]

                            if len(inbound_permission["IpRanges"]) > 0:
                                for ip in inbound_permission["IpRanges"]:
                                    new_inbound_permission_entry = {"Source": ip["CidrIp"], "Protocol": protocol, "Port":to_port}
                                    instance_inbound.append(new_inbound_permission_entry)

                            if len(inbound_permission["Ipv6Ranges"]) > 0:
                                for ipv6 in inbound_permission["Ipv6Ranges"]:
                                    new_inbound_permission_entry = {"Source": ipv6["CidrIpv6"], "Protocol": protocol, "Port":to_port}
                                    instance_inbound.append(new_inbound_permission_entry)
                            
                            if len(inbound_permission["UserIdGroupPairs"]) > 0:
                                for security_group_id in inbound_permission["UserIdGroupPairs"]:
                                    new_inbound_permission_entry = {"Source": security_group_id["GroupId"], "Protocol": protocol, "Port":to_port}
                                    instance_inbound.append(new_inbound_permission_entry)
                            
                            if len(inbound_permission["PrefixListIds"]) > 0:
                                for prefixid in inbound_permission["PrefixListIds"]:
                                    new_inbound_permission_entry = {"Source": prefixid, "Protocol": protocol, "Port":to_port}
                                    instance_inbound.append(new_inbound_permission_entry)
                            
                        for outbound_permission in security_group["IpPermissionsEgress"]:
                            # print(outbound_permission)
                            protocol = outbound_permission["IpProtocol"]
                            from_port = "-1"
                            to_port = "-1"
                            if protocol != "-1":
                                from_port = outbound_permission["FromPort"]
                                to_port = outbound_permission["ToPort"]

                            if len(outbound_permission["IpRanges"]) > 0:
                                for ip in outbound_permission["IpRanges"]:
                                    new_outbound_permission_entry = {"Source": ip["CidrIp"], "Protocol": protocol, "Port":to_port}
                                    instance_outbound.append(new_outbound_permission_entry)

                            if len(outbound_permission["Ipv6Ranges"]) > 0:
                                for ipv6 in outbound_permission["Ipv6Ranges"]:
                                    new_outbound_permission_entry = {"Source": ipv6["CidrIpv6"], "Protocol": protocol, "Port":to_port}
                                    instance_outbound.append(new_outbound_permission_entry)
                            
                            if len(outbound_permission["UserIdGroupPairs"]) > 0:
                                for security_group in outbound_permission["UserIdGroupPairs"]:
                                    new_outbound_permission_entry = {"Source": security_group["GroupId"], "Protocol": protocol, "Port":to_port}
                                    instance_outbound.append(new_outbound_permission_entry)
                            
                            if len(outbound_permission["PrefixListIds"]) > 0:
                                for prefixid in outbound_permission["PrefixListIds"]:
                                    new_outbound_permission_entry = {"Source": prefixid, "Protocol": protocol, "Port":to_port}
                                    instance_outbound.append(new_outbound_permission_entry)
                        
            instance_simplified = {"InstanceID":instance_id, "Name":instance_name,"IPAddress":instance_IP, "Outbound":instance_outbound, "Inbound":instance_inbound}
            instance_data.append(instance_simplified)
        

    instances = {"Instances":instance_data}
    return instances
