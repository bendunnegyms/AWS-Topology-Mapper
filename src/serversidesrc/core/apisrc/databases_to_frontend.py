import json

def databases_to_frontend_format(security_groups_data, database_data):

    instances = database_data["DBInstances"]
    sg_data_list = security_groups_data["SecurityGroups"]

    instance_data = []

    for instance in instances:

        instance_id = instance["DBInstanceIdentifier"]
        instance_sgs = []   
        for sg_data in instance["VpcSecurityGroups"]:
            instance_sgs.append(sg_data["VpcSecurityGroupId"])

        #print(instance_sgs)
        instance_inbound = []
        instance_outbound = []
        instance_subnets = []


        for sg in instance_sgs:
            # sg_id = sg["GroupId"]
            for security_group in sg_data_list:
                if sg == security_group["GroupId"]:
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
                                if new_inbound_permission_entry not in instance_inbound:
                                    instance_inbound.append(new_inbound_permission_entry)

                        if len(inbound_permission["Ipv6Ranges"]) > 0:
                            for ipv6 in inbound_permission["Ipv6Ranges"]:
                                new_inbound_permission_entry = {"Source": ipv6["CidrIpv6"], "Protocol": protocol, "Port":to_port}
                                if new_inbound_permission_entry not in instance_inbound:
                                    instance_inbound.append(new_inbound_permission_entry)
                        
                        if len(inbound_permission["UserIdGroupPairs"]) > 0:
                            for security_group_id in inbound_permission["UserIdGroupPairs"]:
                                new_inbound_permission_entry = {"Source": security_group_id["GroupId"], "Protocol": protocol, "Port":to_port}
                                if new_inbound_permission_entry not in instance_inbound:
                                    instance_inbound.append(new_inbound_permission_entry)
                        
                        if len(inbound_permission["PrefixListIds"]) > 0:
                            for prefixid in inbound_permission["PrefixListIds"]:
                                new_inbound_permission_entry = {"Source": prefixid, "Protocol": protocol, "Port":to_port}
                                if new_inbound_permission_entry not in instance_inbound:
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
                                if new_outbound_permission_entry not in instance_outbound:
                                    instance_outbound.append(new_outbound_permission_entry)

                        if len(outbound_permission["Ipv6Ranges"]) > 0:
                            for ipv6 in outbound_permission["Ipv6Ranges"]:
                                new_outbound_permission_entry = {"Source": ipv6["CidrIpv6"], "Protocol": protocol, "Port":to_port}
                                if new_outbound_permission_entry not in instance_outbound:
                                    instance_outbound.append(new_outbound_permission_entry)
                        
                        if len(outbound_permission["UserIdGroupPairs"]) > 0:
                            for security_group in outbound_permission["UserIdGroupPairs"]:
                                new_outbound_permission_entry = {"Source": security_group["GroupId"], "Protocol": protocol, "Port":to_port}
                                if new_outbound_permission_entry not in instance_outbound:
                                    instance_outbound.append(new_outbound_permission_entry)
                        
                        if len(outbound_permission["PrefixListIds"]) > 0:
                            for prefixid in outbound_permission["PrefixListIds"]:
                                new_outbound_permission_entry = {"Source": prefixid, "Protocol": protocol, "Port":to_port}
                                if new_outbound_permission_entry not in instance_outbound:
                                    instance_outbound.append(new_outbound_permission_entry)
        
    
        

        instance_simplified = {"DB_id":instance_id, "SecurityGroups":instance_sgs,"Outbound":instance_outbound, "Inbound":instance_inbound}
        instance_data.append(instance_simplified)
        

    instances = {"Databases":instance_data}
    return instances
