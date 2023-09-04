Terraform code is designed to deploy AWS ECS with fargate to run stateless application

Prerequisites 
AWS Account with AWS CLI installed in system or any cloud instance connected to aws account
you can configure connection using aws cli - aws configure command.
the user should have sufficient permission to provision iam, ecs, vpc and alb components.


terraform need to be installed on the system.
Refer https://developer.hashicorp.com/terraform/downloads 

Once aws account is connected to the system and terraform installed you can clone the code from github URL and execute below commands to deploy the code. 
URL:

execute the script in terminal : ./infra_deploy.sh
or run below commands manually 

terraform init
terraform plan
terraform apply --auto-approve

verify aws loadbalancer DNS to verify the nginx page or curl the DNS 
once you verify the part and not using the infrastructure then  run 'terraform destroy --auto-approve' to delete infra to avoid unnecessary billing. 

Diagram as Code
https://diagrams.mingrammer.com/docs/getting-started/installation

1.  It requires Python 3.6 or higher, check your Python version first.
2.  It uses Graphviz to render the diagram, so you need to install Graphviz to use diagrams
    https://graphviz.gitlab.io/download/ 
    eg: sudo apt install graphviz
3.  # using pip (pip3)
    $ pip install diagrams

4.  create a architecture_diagram.py file and use python to create diagram 

Summary

The Terraform code provided creates a basic AWS infrastructure setup with a Virtual Private Cloud (VPC), public subnets, an internet gateway, routing tables, and an Elastic Load Balancer (ELB) for an Elastic Container Service (ECS) Fargate deployment. Here's a high-level description of the traffic flow and resources:

Terraform and AWS Provider Configuration:
Specifies that the AWS provider of version ~> 5.4.0 is required.
Configures the AWS provider to use the region specified in var.region.

Network Configuration:
Creates a VPC with a CIDR block of 10.0.0.0/16.
Creates two public subnets within the VPC, one in the us-east-1a availability zone and the other in us-east-1b.
Creates an Internet Gateway (igw) and attaches it to the VPC.
A public routing table is created, specifying that traffic to 0.0.0.0/0 (all IPs) should go through the Internet Gateway, essentially enabling internet access for resources associated with this route table.
Associates the public subnets with the public route table.

Security Configuration:
Defines a security group that allows inbound HTTP traffic (port 80) from anywhere (0.0.0.0/0). All outbound traffic is also allowed.

Load Balancer Configuration:
Deploys an Application Load Balancer (ALB) in both public subnets and associates it with the previously defined security group.
Defines a target group for the ALB, which determines where to route requests.
Specifies a listener for the ALB on port 80 that forwards traffic to the target group.

IAM Role and Policy Configuration:
Two IAM roles (ecs_task_role and ecs_execution_role) are defined for ECS tasks. These roles specify what AWS services the ECS tasks are allowed to interact with.
Attaches a policy (ecs_task_policy) to ecs_task_role that grants permissions to create log streams and put log events in AWS CloudWatch.
Attaches the built-in AWS policy AmazonECSTaskExecutionRolePolicy to the ecs_execution_role, which provides the ECS tasks the permissions they need to interact with other AWS services.

ECS Configuration:
Creates an ECS cluster.
Defines an ECS task definition for a Fargate task. The task uses the nginxdemos/hello image from Docker Hub to run an Nginx server.


Creates an ECS service that deploys the defined task in the public subnets. The service uses the previously defined security group and is associated with the ALB's target group. This means that any traffic coming to the ALB will be forwarded to one of the running ECS tasks.


Traffic Flow:
External traffic can access the ECS service through the ALB's DNS.
The ALB receives the traffic and forwards it to one of the ECS tasks in the target group based on its load balancing algorithm.
The ECS task, which runs an Nginx container, handles the traffic.
The response from the ECS task flows back through the ALB to the user.
This setup is typical for deploying web applications in AWS using ECS Fargate, where you want to ensure high availability by deploying across multiple availability zones and distributing traffic using an ALB.


![Example Image](https://github.com/nixvarghese01/ecs-stateless-nginx/blob/dev/aws_infrastructure.png)
