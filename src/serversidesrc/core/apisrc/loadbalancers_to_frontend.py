import json

def load_balancers_to_frontend_format(security_groups_data, load_balancers_data):

    sg_data_list = security_groups_data["SecurityGroups"]
    

    balancer_data = []


    data = load_balancers_data["LoadBalancerDescriptions"]

    for entry in data:
        balancerName = entry["LoadBalancerName"]              #"Name"
        source_sg_group = entry["SourceSecurityGroup"]                            
        sg_name = source_sg_group["GroupName"]                #"securityGroup"
        balancer_sgs = entry["SecurityGroups"]

        balancer_instances = []  
        listeners = []

        instance_outbound = []
        instance_inbound = []
        
        #fills balancer_instance_ids
        for instance in entry["Instances"]:
            new_instance_ID = {"InstanceId": instance["InstanceId"]}
            balancer_instances.append(new_instance_ID)

        listener_descriptions = entry["ListenerDescriptions"]

        #fills listener data
        for listener in listener_descriptions:
            current_listener = listener["Listener"]

            
            protocol = current_listener["Protocol"]
            balancer_port = current_listener["LoadBalancerPort"]
            target_protocol = current_listener["InstanceProtocol"]
            target_port = current_listener["InstancePort"]

            new_listener_entry = {"LoadBalancerSideProtocol": protocol, "LoadBalancerSidePort": balancer_port, "TargetProtocol": target_protocol, "TargetPort": target_port}

            listeners.append(new_listener_entry)

        # this can be ripped for creating inbound and outbound lists for rds, load balancers, etc, 
        #for sg in sg_name:
            sg_id = sg_name
            for security_group in sg_data_list:
                if sg_id == security_group["GroupName"]:
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

        balancer_simplified = {"Name":balancerName, "Instance_ids": balancer_instances, "SecurityGroup":sg_name, "Inbound":instance_inbound, "Outbound":instance_outbound, "Listeners":listeners }
        balancer_data.append(balancer_simplified)

    balancers ={"LoadBalancers":balancer_data}
    return balancers

