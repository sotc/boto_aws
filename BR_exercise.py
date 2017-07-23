#!/usr/bin/python

import os
import sys
import boto3
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--instance_name', nargs='?', default='prod-br-app-s2', help='search for a specific instance, defaults to prod-br-app-s2')
    parser.add_argument('--aws_region', nargs='?', default='us-west-2', help='choose a region, defaults to us-west-2')
    parser.add_argument('--list_regions', action='store_true', help='display a list of regions')
    parser.add_argument('--list_all_ec2s', action='store_true', help='display a list instance in every regions')
    args = parser.parse_args()
    return args

def list_all_instances(aws_resource):
    for region in get_regions(aws_client):
        #print region
        #ec2_resource = boto3.resource('ec2', region_name=region)
        ec2_resource = aws_resource
    #for instance in aws_resource.instances.all():
        for instance in ec2_resource.instances.all():
            instance, instance.tag
    print("nothing here but us birds")

def filter_instance(aws_resource):
    filter_name = parse_args().instance_name
    print filter_name
    filters = [{'Name':'tag:Name', 'Values':[filter_name]}]
    my_instance = list(aws_resource.vpcs.filter(Filters=filters)) 
    print my_instance

def get_regions(aws_client):
    print("from a funct:", parse_args().aws_region) 
    region_desc = []
    regions = aws_client.describe_regions().get('Regions', [])
    for region in regions:
        #print region
        region_desc.append(region['RegionName'])
    #print region_desc
    return region_desc

def main():
    parse_args()
    if parse_args().list_all_ec2s:
        list_all_instances(aws_resource)
    elif parse_args().instance_name:
        filter_instance(aws_resource)

if __name__ == '__main__':

    aws_region = parse_args().aws_region
    aws_client = boto3.client('ec2', region_name=aws_region)
    aws_resource = boto3.resource('ec2', region_name=aws_region)
    if not parse_args().list_regions:
        main()
    else: 
        print get_regions(aws_client)
