import json

def databases_to_frontend_format(database_data, instances_data):

    data_list = database_data["Databases"]

    instance_data = []
    data = instances_data["Reservations"]

    for entry in data:
        instances = entry["Instances"] #- gives list
        for instance in instances:

            instance_id = instance["DB_id"]
            instance_class = instance["DB_class"]
            instance_status = instance["Status"]
            instance_engine = instance["Engine"]

            instance_endpoint = []

            instance_inbound = []
            instance_outbound = []
            instance_subnets = []

            endpoint_data = instance["Endpoint"]
            endpoint_simplified = {"Address": endpoint_data["Address"], "Port":endpoint_data["Port"]}


            for inbound_data in database_data:
                            
                protocol = inbound_data["IpProtocol"]
                from_port = "-1"
                to_port = "-1"
                if protocol != "-1":
                    from_port = inbound_data["FromPort"]
                    to_port = inbound_data["ToPort"]

                if len(inbound_data["IpRanges"]) > 0:
                    for ip in inbound_data["IpRanges"]:
                        new_inbound_data_entry = {"Source": ip["CidrIp"], "Port":to_port, "Protocol": protocol}
                        if new_inbound_data_entry not in instance_inbound:
                            instance_inbound.append(new_inbound_data_entry)

                        if len(inbound_data["Ipv6Ranges"]) > 0:
                            for ipv6 in inbound_data["Ipv6Ranges"]:
                                new_inbound_data_entry = {"Source": ipv6["CidrIpv6"], "Port":to_port, "Protocol": protocol}
                                if new_inbound_data_entry not in instance_inbound:
                                    instance_inbound.append(new_inbound_data_entry)
                        
                        if len(inbound_data["UserIdGroupPairs"]) > 0:
                            for security_group_id in inbound_data["UserIdGroupPairs"]:
                                new_inbound_data_entry = {"Source": security_group_id["GroupId"], "Port":to_port ,"Protocol": protocol}
                                if new_inbound_data_entry not in instance_inbound:
                                    instance_inbound.append(new_inbound_data_entry)

                            
                    for outbound_data in database_data:
                        
                        protocol = outbound_data["IpProtocol"]
                        from_port = "-1"
                        to_port = "-1"
                        if protocol != "-1":
                            from_port = outbound_data["FromPort"]
                            to_port = outbound_data["ToPort"]

                        if len(outbound_data["IpRanges"]) > 0:
                            for ip in outbound_data["IpRanges"]:
                                new_outbound_data_entry = {"Destination": ip["CidrIp"], "Port":to_port, "Protocol": protocol}
                                if new_outbound_data_entry not in instance_outbound:
                                    instance_outbound.append(new_outbound_data_entry)

                        if len(outbound_data["Ipv6Ranges"]) > 0:
                            for ipv6 in outbound_data["Ipv6Ranges"]:
                                new_outbound_data_entry = {"Destination": ipv6["CidrIpv6"], "Port":to_port, "Protocol": protocol}
                                if new_outbound_data_entry not in instance_outbound:
                                    instance_outbound.append(new_outbound_data_entry)
                        
                        if len(outbound_data["UserIdGroupPairs"]) > 0:
                            for security_group in outbound_data["UserIdGroupPairs"]:
                                new_outbound_data_entry = {"Destination": security_group["GroupId"], "Port":to_port, "Protocol": protocol}
                                if new_outbound_data_entry not in instance_outbound:
                                    instance_outbound.append(new_outbound_data_entry)
                        
                        if len(outbound_data["PrefixListIds"]) > 0:
                            for prefixid in outbound_data["PrefixListIds"]:
                                new_outbound_data_entry = {"Destination": prefixid, "Port":to_port, "Protocol": protocol}
                                if new_outbound_data_entry not in instance_outbound:
                                    instance_outbound.append(new_outbound_data_entry)

            subnet_data = instance["DBSubnetGroup"]["Subnets"]
            for subnet in subnet_data:
            	new_subnet_data_entry = {"Subnet_id":subnet["SubnetIdentifier"], "SubnetAvailabilityZone":subnet["SubnetAvailabilityZone"]["Name"], "Status":subnet["SubnetStatus"]}
                if new_subnet_data_entry not in subnets_list:
                    instance_subnets.append(new_subnet_data_entry)
            

        instance_simplified = {"DB_id":instance_id, "DB_class":instance_class,"Status":instance_status, "Engine":instance_engine, "Outbound":instance_outbound, "Inbound":instance_inbound, "Subnets": subnets_list, "Endpoint": endpoint_simplified}
        instance_data.append(instance_simplified)
        

    instances = {"Databases":instance_data}
    return instances
