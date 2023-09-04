from diagrams import Diagram, Cluster
from diagrams.aws.compute import ECS, EC2
from diagrams.aws.network import VPC, ALB, RouteTable, InternetGateway, PublicSubnet
from diagrams.aws.security import IAMRole

with Diagram("AWS Infrastructure", show=False, direction="TB"):

    # Define VPC and its related networking components
    with Cluster("Virtual Private Cloud"):
        vpc = VPC("VPC\n10.0.0.0/16")
        
        # Public Subnets and related resources
        with Cluster("Public Subnets"):
            subnet1 = PublicSubnet("Subnet 1\n10.0.1.0/24\nus-east-1a")
            subnet2 = PublicSubnet("Subnet 2\n10.0.2.0/24\nus-east-1b")
            igw = InternetGateway("Internet GW")
            route_table = RouteTable("Public Route Table")
            
            # Connect networking components
            vpc >> igw  # VPC connects to Internet Gateway
            igw >> route_table  # Internet Gateway connects to Route Table
            route_table >> subnet1  # Route table routes traffic for subnet1
            route_table >> subnet2  # Route table routes traffic for subnet2

        # Security Group
        sg = EC2("Web Server SG\nallow_http")
        egress = EC2("Egress SG\nallow_all")
        
        # Connect Security Groups
        sg >> igw  # Ingress: Allow incoming traffic from the internet
        sg << egress  # Egress: Allow outgoing traffic to anywhere

    # Define Load Balancer components
    with Cluster("Load Balancer"):
        alb = ALB("Web ALB")
        alb_target_group = EC2("Target Group\nweb-tg")
        alb_listener = EC2("Listener\nHTTP")
        
        # Connect Load Balancer components
        alb >> alb_target_group  # ALB forwards requests to the target group
        alb_target_group >> alb_listener  # Target group sends traffic to the listener

    # Define ECS components and related IAM roles
    with Cluster("ECS Services"):
        ecs_role = IAMRole("Task Role")
        ecs_execution_role = IAMRole("Execution Role")
        ecs_cluster = ECS("Cluster\nmy-ecs-cluster")
        ecs_task = ECS("Task\nmy-task-def")
        ecs_service = ECS("Web Server Service")
        
        # Connect ECS components and IAM roles
        ecs_role >> ecs_task  # Task uses ECS role for permissions
        ecs_execution_role >> ecs_task  # Task uses execution role for AWS service integrations
        ecs_task >> ecs_service  # Service uses a specific task definition
        ecs_service >> ecs_cluster  # Service runs within a cluster
        
        ecs_service - alb_listener  # Service traffic is routed through the ALB

    route_table - alb  # Traffic from the route table is routed through the ALB based on the subnet zone

