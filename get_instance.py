#!/usr/bin/python

import boto
import boto.ec2
import csv_file
from boto.ec2.regioninfo import RegionInfo



def get_regions():
    '''
    Returns a list of all valid regions for our EC2 service.
    Excludes any regions we do not have access to.
    '''
    region_name = []
    for region in boto.ec2.regions():
        #print region.name
        if region.name not in ['cn-north-1', 'us-gov-west-1']:
            region_name.append(region.name)
    #print region_name
    return region_name

def get_vol_details(instance_id, ec2_conn):
    '''
    Returns a dictionary of volume ids and volume sizes associated with 
    instance ids. 
    '''
    ec2_conn = ec2_conn
    vol_details = []
    for vol in ec2_conn.get_all_volumes(filters={'attachment.instance-id': instance_id}):
        #print vol
        vol_details.append({'vol_id': vol.id, 'vol_size': vol.size})

    return vol_details

def get_ec2_instances():
    '''
    Retruns a dictionary of all instances associated with our EC2 service.
    The dictionary includes details of the instance along with their 
    attached volumes. It's then passed into the csv_file module
    to wirte out a csv file.
    '''
    instance_details = []
    for region in get_regions():
        #print region
        ec2_conn = boto.ec2.connect_to_region(region)
        #print ec2_conn
        for instance in ec2_conn.get_only_instances():
            #print instance
            vol_details = get_vol_details(instance.id, ec2_conn)
            for detail in vol_details:
                #import pdb; pdb.set_trace()
                detail.update({'id': instance.id, 'type' : instance.instance_type, 'state' : instance.state})
                instance_details.append(detail)

    return instance_details


def main():
    #print get_regions()
    #get_ec2_instances()
    csv_file.write_csv("instance_info.csv", get_ec2_instances())

if __name__ == '__main__':
    main()
