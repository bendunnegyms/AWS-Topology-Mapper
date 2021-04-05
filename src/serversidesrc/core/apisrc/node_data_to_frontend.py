import json 

def createNodeData(all_instance_data):

    ec2_instances = all_instance_data["Instances"]
    balancers = all_instance_data["LoadBalancers"]
    databases = all_instance_data["Databases"]
    app_balancers = all_instance_data["AppBalancers"]


    nodes = []
    outward_links = []

    #NODE CREATION
    #loop through each instance
    for entry in ec2_instances:
        #save instance data
        instance_id = entry["InstanceID"]
        instance_name = entry["Name"]
        instance_sg = []

        sg_data = entry["SecurityGroups"]
        for sg_group in sg_data:
            sg = sg_group["GroupName"]
            instance_sg.append(sg)
        

        instance_simplified = {"instanceID":instance_id, "name":instance_name, "type": "ec2", "securityGroups":instance_sg}
        nodes.append(instance_simplified)

    #loop through each balancer
    for entry in balancers:
        # balancer_id = entry["InstanceID"] #these id's are the ec2 id's it can communicate with
        balancer_name = entry["Name"]
        balancer_sgs = []

        sg_data = entry["SecurityGroups"]
        for sg_group in sg_data:
            sg = sg_group["GroupName"]
            balancer_sgs.append(sg)

        balancer_simplified = {"name":balancer_name, "type": "loadBalancer", "securityGroups":balancer_sgs}
        nodes.append(balancer_simplified)

    #loop through each app_balancer
    for entry in app_balancers:
        # balancer_id = entry["InstanceID"] #these id's are the ec2 id's it can communicate with
        balancer_name = entry["Name"]
        balancer_ARN = entry["BalancerARN"]
        balancer_sgs = []

        sg_data = entry["SecurityGroups"]
        for sg_group in sg_data:
            sg = sg_group["GroupName"]
            balancer_sgs.append(sg)

        app_balancer_simplified = {"name":balancer_name, "arn": balancer_ARN, "type":"appBalancer", "securityGroups":balancer_sgs}
        nodes.append(app_balancer_simplified)

    #loop through each database
    for entry in databases:
        database_id = entry["DB_id"]
        database_name = entry["DB_name"]
        sg_data = entry["SecurityGroups"]
        database_sgs = []
        for data in sg_data:
            sg_name = data["GroupName"]
            database_sgs.append(sg_name)

        database_simplified = {"instanceID":database_id, "name":database_name, "type": "database", "securityGroups": database_sgs}
        nodes.append(database_simplified)


    #LINK CREATION
    #ec2 connections
    
    #ec2 -> ec2
    for entry in ec2_instances:
        source_instance_id = entry["InstanceID"]
        outbound_connections = entry["Outbound"]
        for outbound in outbound_connections:
            
            #outbound details for source node
            outbound_destination = outbound["Destination"]
            outbound_protocol = outbound["Protocol"]
            outbound_port = outbound["Port"]
           
            #loop to check all other ec2 instances
            for data in ec2_instances:
                destination_instance_id = data["InstanceID"]
                inbound_connections = data["Inbound"]

                if ((destination_instance_id)!=(source_instance_id)):
                    for inbound in inbound_connections:

                        #inbound details for destination node
                        inbound_source = inbound["Source"]
                        inbound_protocol = inbound["Protocol"]
                        inbound_port = inbound["Port"]

                        if(outbound_destination==inbound_source):
                            if((inbound_protocol==outbound_protocol) or (outbound_protocol == -1)):
                                if((inbound_port==outbound_port) or (outbound_port == -1)):

                                    connection_data = {"source":inbound_source, "protocol":inbound_protocol,"port":inbound_port}

                                    instance_link = {"source":source_instance_id, "target":destination_instance_id, "info":connection_data}
                                    outward_links.append(instance_link)
    
    #ec2 -> loadBalancers
    for entry in ec2_instances:
        source_instance_id = entry["InstanceID"]
        outbound_connections = entry["Outbound"]
        for outbound in outbound_connections:
        
            #outbound details for source node
            outbound_destination = outbound["Destination"]
            outbound_protocol = outbound["Protocol"]
            outbound_port = outbound["Port"]

            for data in balancers:
                destination_instance_id = data["Name"]
                inbound_connections = data["Inbound"]

                for inbound in inbound_connections:

                    #inbound details for destination node
                    inbound_source = inbound["Source"]
                    inbound_protocol = inbound["Protocol"]
                    inbound_port = inbound["Port"]

                    if(outbound_destination==inbound_source):
                        if((inbound_protocol==outbound_protocol) or (outbound_protocol == -1)):
                            if((inbound_port==outbound_port) or (outbound_port == -1)):

                                connection_data = {"source":inbound_source, "protocol":inbound_protocol,"port":inbound_port}
                                
                                instance_link = {"source":source_instance_id, "target":destination_instance_id, "info":connection_data}
                                outward_links.append(instance_link)

    #ec2 -> appbalancers
    for entry in ec2_instances:
        source_instance_id = entry["InstanceID"]
        outbound_connections = entry["Outbound"]
        for outbound in outbound_connections:
        
            #outbound details for source node
            outbound_destination = outbound["Destination"]
            outbound_protocol = outbound["Protocol"]
            outbound_port = outbound["Port"]

            for data in app_balancers:
                destination_instance_id = data["BalancerARN"]
                inbound_connections = data["Inbound"]

                for inbound in inbound_connections:

                    #inbound details for destination node
                    inbound_source = inbound["Source"]
                    inbound_protocol = inbound["Protocol"]
                    inbound_port = inbound["Port"]

                    if(outbound_destination==inbound_source):
                        if((inbound_protocol==outbound_protocol) or (outbound_protocol == -1)):
                            if((inbound_port==outbound_port) or (outbound_port == -1)):

                                connection_data = {"source":inbound_source, "protocol":inbound_protocol,"port":inbound_port}
                                
                                instance_link = {"source":source_instance_id, "target":destination_instance_id, "info":connection_data}
                                outward_links.append(instance_link)

    #ec2 -> databases
    for entry in ec2_instances:
        source_instance_id = entry["InstanceID"]
        outbound_connections = entry["Outbound"]
        for outbound in outbound_connections:
        
            #outbound details for source node
            outbound_destination = outbound["Destination"]
            outbound_protocol = outbound["Protocol"]
            outbound_port = outbound["Port"]

            for data in databases:
                destination_instance_id = data["DB_id"]
                inbound_connections = data["Inbound"]

                for inbound in inbound_connections:

                    #inbound details for destination node
                    inbound_source = inbound["Source"]
                    inbound_protocol = inbound["Protocol"]
                    inbound_port = inbound["Port"]

                    if(outbound_destination==inbound_source):
                        if((inbound_protocol==outbound_protocol) or (outbound_protocol == -1)):
                            if((inbound_port==outbound_port) or (outbound_port == -1)):

                                connection_data = {"source":inbound_source, "protocol":inbound_protocol,"port":inbound_port}
                                
                                instance_link = {"source":source_instance_id, "target":destination_instance_id, "info":connection_data}
                                outward_links.append(instance_link)



    #loadbalancer connections

    #loadBalancer -> loadBalancer
    for entry in balancers:
        source_instance_id = entry["Name"]
        outbound_connections = entry["Outbound"]
        for outbound in outbound_connections:
        
            #outbound details for source node
            outbound_destination = outbound["Destination"]
            outbound_protocol = outbound["Protocol"]
            outbound_port = outbound["Port"]

            for data in balancers:
                destination_instance_id = data["Name"]
                inbound_connections = data["Inbound"]

                if ((destination_instance_id)!=(source_instance_id)):
                    for inbound in inbound_connections:

                        #inbound details for destination node
                        inbound_source = inbound["Source"]
                        inbound_protocol = inbound["Protocol"]
                        inbound_port = inbound["Port"]

                        if(outbound_destination==inbound_source):
                            if((inbound_protocol==outbound_protocol) or (outbound_protocol == -1)):
                                if((inbound_port==outbound_port) or (outbound_port == -1)):

                                    connection_data = {"source":inbound_source, "protocol":inbound_protocol,"port":inbound_port}
                                   
                                    instance_link = {"source":source_instance_id, "target":destination_instance_id, "info":connection_data}
                                    outward_links.append(instance_link)


    #loadbalancer -> ec2
    for entry in balancers:
        source_instance_id = entry["Name"]
        outbound_connections = entry["Outbound"]
        for outbound in outbound_connections:
        
            #outbound details for source node
            outbound_destination = outbound["Destination"]
            outbound_protocol = outbound["Protocol"]
            outbound_port = outbound["Port"]

            #loop to check all other ec2 instances
            for data in ec2_instances:
                destination_instance_id = data["InstanceID"]
                inbound_connections = data["Inbound"]

               
                
                if ((destination_instance_id)!=(source_instance_id)):
                    for inbound in inbound_connections:

                        #inbound details for destination node
                        inbound_source = inbound["Source"]
                        inbound_protocol = inbound["Protocol"]
                        inbound_port = inbound["Port"]

                        if(outbound_destination==inbound_source):
                            if((inbound_protocol==outbound_protocol) or (outbound_protocol == -1)):
                                if((inbound_port==outbound_port) or (outbound_port == -1)):

                                    connection_data = {"source":inbound_source, "protocol":inbound_protocol,"port":inbound_port}
                                    
                                    instance_link = {"source":source_instance_id, "target":destination_instance_id, "info":connection_data}
                                    outward_links.append(instance_link)
                               
    #loadbalancer -> appbalancer
    for entry in balancers:
        source_instance_id = entry["Name"]
        outbound_connections = entry["Outbound"]
        for outbound in outbound_connections:
        
            #outbound details for source node
            outbound_destination = outbound["Destination"]
            outbound_protocol = outbound["Protocol"]
            outbound_port = outbound["Port"]

            for data in app_balancers:
                destination_instance_id = data["BalancerARN"]
                inbound_connections = data["Inbound"]

                for inbound in inbound_connections:

                    #inbound details for destination node
                    inbound_source = inbound["Source"]
                    inbound_protocol = inbound["Protocol"]
                    inbound_port = inbound["Port"]

                    if(outbound_destination==inbound_source):
                        if((inbound_protocol==outbound_protocol) or (outbound_protocol == -1)):
                            if((inbound_port==outbound_port) or (outbound_port == -1)):

                                connection_data = {"source":inbound_source, "protocol":inbound_protocol,"port":inbound_port}
                                
                                instance_link = {"source":source_instance_id, "target":destination_instance_id, "info":connection_data}
                                outward_links.append(instance_link)
                               

    #loadbalancer -> database
    for entry in balancers:
        source_instance_id = entry["Name"]
        outbound_connections = entry["Outbound"]
        for outbound in outbound_connections:
        
            #outbound details for source node
            outbound_destination = outbound["Destination"]
            outbound_protocol = outbound["Protocol"]
            outbound_port = outbound["Port"]

            for data in databases:
                destination_instance_id = data["DB_id"]
                inbound_connections = data["Inbound"]


                for inbound in inbound_connections:

                    #inbound details for destination node
                    inbound_source = inbound["Source"]
                    inbound_protocol = inbound["Protocol"]
                    inbound_port = inbound["Port"]

                    if(outbound_destination==inbound_source):
                        if((inbound_protocol==outbound_protocol) or (outbound_protocol == -1)):
                            if((inbound_port==outbound_port) or (outbound_port == -1)):

                                connection_data = {"source":inbound_source, "protocol":inbound_protocol,"port":inbound_port}
                                
                                instance_link = {"source":source_instance_id, "target":destination_instance_id, "info":connection_data}
                                outward_links.append(instance_link)



    #appbalancer connections
     
    #appbal -> appbal
    for entry in app_balancers:
        source_instance_id = entry["BalancerARN"]
        outbound_connections = entry["Outbound"]
        for outbound in outbound_connections:
        
            #outbound details for source node
            outbound_destination = outbound["Destination"]
            outbound_protocol = outbound["Protocol"]
            outbound_port = outbound["Port"]

            for data in app_balancers:
                destination_instance_id = data["BalancerARN"]
                inbound_connections = data["Inbound"]

                if ((destination_instance_id)!=(source_instance_id)):
                    for inbound in inbound_connections:

                        #inbound details for destination node
                        inbound_source = inbound["Source"]
                        inbound_protocol = inbound["Protocol"]
                        inbound_port = inbound["Port"]

                        if(outbound_destination==inbound_source):
                            if((inbound_protocol==outbound_protocol) or (outbound_protocol == -1)):
                                if((inbound_port==outbound_port) or (outbound_port == -1)):

                                    connection_data = {"source":inbound_source, "protocol":inbound_protocol,"port":inbound_port}
                                    
                                    instance_link = {"source":source_instance_id, "target":destination_instance_id, "info":connection_data}
                                    outward_links.append(instance_link)
     
    #appbal -> ec2
    for entry in app_balancers:
        source_instance_id = entry["BalancerARN"]
        outbound_connections = entry["Outbound"]
        for outbound in outbound_connections:
        
            #outbound details for source node
            outbound_destination = outbound["Destination"]
            outbound_protocol = outbound["Protocol"]
            outbound_port = outbound["Port"]

            #loop to check all other ec2 instances
            for data in ec2_instances:
                destination_instance_id = data["InstanceID"]
                inbound_connections = data["Inbound"]

                if ((destination_instance_id)!=(source_instance_id)):
                    for inbound in inbound_connections:

                        #inbound details for destination node
                        inbound_source = inbound["Source"]
                        inbound_protocol = inbound["Protocol"]
                        inbound_port = inbound["Port"]

                        if(outbound_destination==inbound_source):
                            if((inbound_protocol==outbound_protocol) or (outbound_protocol == -1)):
                                if((inbound_port==outbound_port) or (outbound_port == -1)):

                                    connection_data = {"source":inbound_source, "protocol":inbound_protocol,"port":inbound_port}
                                    
                                    instance_link = {"source":source_instance_id, "target":destination_instance_id, "info":connection_data}
                                    outward_links.append(instance_link)


    #appbal -> loadbal
    for entry in app_balancers:
        source_instance_id = entry["BalancerARN"]
        outbound_connections = entry["Outbound"]
        for outbound in outbound_connections:
        
            #outbound details for source node
            outbound_destination = outbound["Destination"]
            outbound_protocol = outbound["Protocol"]
            outbound_port = outbound["Port"]

            for data in balancers:
                destination_instance_id = data["Name"]
                inbound_connections = data["Inbound"]

                for inbound in inbound_connections:

                    #inbound details for destination node
                    inbound_source = inbound["Source"]
                    inbound_protocol = inbound["Protocol"]
                    inbound_port = inbound["Port"]

                    if(outbound_destination==inbound_source):
                        if((inbound_protocol==outbound_protocol) or (outbound_protocol == -1)):
                            if((inbound_port==outbound_port) or (outbound_port == -1)):

                                connection_data = {"source":inbound_source, "protocol":inbound_protocol,"port":inbound_port}
                                
                                instance_link = {"source":source_instance_id, "target":destination_instance_id, "info":connection_data}
                                outward_links.append(instance_link)

    #appbak -> database
    for entry in app_balancers:
        source_instance_id = entry["BalancerARN"]
        outbound_connections = entry["Outbound"]
        for outbound in outbound_connections:
        
            #outbound details for source node
            outbound_destination = outbound["Destination"]
            outbound_protocol = outbound["Protocol"]
            outbound_port = outbound["Port"]

            for data in databases:
                destination_instance_id = data["DB_id"]
                inbound_connections = data["Inbound"]


                for inbound in inbound_connections:

                    #inbound details for destination node
                    inbound_source = inbound["Source"]
                    inbound_protocol = inbound["Protocol"]
                    inbound_port = inbound["Port"]

                    if(outbound_destination==inbound_source):
                        if((inbound_protocol==outbound_protocol) or (outbound_protocol == -1)):
                            if((inbound_port==outbound_port) or (outbound_port == -1)):

                                connection_data = {"source":inbound_source, "protocol":inbound_protocol,"port":inbound_port}
                                
                                instance_link = {"source":source_instance_id, "target":destination_instance_id, "info":connection_data}
                                outward_links.append(instance_link)                          

    #links.append(outward_links)
    nodeJson = {"nodes": nodes, "links": outward_links}
    return nodeJson