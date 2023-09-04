#!/bin/bash

# Initialize the Terraform environment
terraform init
if [ $? -ne 0 ]; then
  echo "Terraform initialization failed!"
  exit 1
fi

# Validate the Terraform configuration files
terraform validate
if [ $? -ne 0 ]; then
  echo "Terraform validation failed!"
  exit 1
fi

# Plan the Terraform changes
terraform plan -out=tfplan
if [ $? -ne 0 ]; then
  echo "Terraform planning failed!"
  exit 1
fi

# Apply the Terraform changes
terraform apply -auto-approve tfplan
if [ $? -ne 0 ]; then
  echo "Terraform apply failed!"
  exit 1
fi

echo "Terraform deployment was successful!"
terraform output load_balancer_dns_name
