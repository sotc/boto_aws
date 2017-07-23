"""
S3 Utilities

Actions To Perform:

Download from s3 function

Upload to s3 function

"""

import boto3
#from boto3.s3.transfer import S3Transfer
from sensible.loginit import logger

log = logger(__name__)
REGION = 'us-west-2'

def s3_client():
    """Establishes S3 client connection"""

    client = boto3.client('s3', region_name=REGION)
    log.info("Connection established for s3")
    return client

def s3_resource():
    """Establishes s3 resource connection"""

    resource = boto3.resource('s3')
    log.info("Resource established for s3")
    return resource

###S3 Resources
def list_buckets():
    """ Retrieves a list of buckets
    """

    buckets = []
    s3resource = s3_resource()
    log_msg = "Listing all s3 buckets"
    log.info(log_msg)
    for bucket in s3resource.buckets.all():
        buckets.append(bucket.name)
    return buckets

def get_files(bucket, subdir):
    """ 
    Returns a list of files
    """

    sub_files = []
    s3client = s3_client()
    paginator = s3client.get_paginator('list_objects_v2')
    for result in paginator.paginate(Bucket=bucket, Delimiter='/', Prefix=subdir):
        if result.get('Contents') is not None:
            for files in result.get('Contents'):
                if not files.get('Key') == "":
                    sub_files.append(files.get('Key'))
    return sub_files

sub_folders = []
def get_subdir(bucket, subdir):
    """ 
    Returns sub directories from a bucket. Global list sub_folders
    """

    s3client = s3_client()
    paginator = s3client.get_paginator('list_objects_v2')
    for result in paginator.paginate(Bucket=bucket, Delimiter='/', Prefix=subdir):
        if result.get('CommonPrefixes') is not None:
            for subdir in result.get('CommonPrefixes'):
                #print "get_subdir(): " + subdir.get('Prefix')
                sub_folders.append(subdir.get('Prefix'))
                get_subdir(bucket, subdir.get('Prefix'))
    return sub_folders

def get_top_dirs(bucket):
    """
    Retrieve only the top level directories in a bucket
    """

    parent_dir = []
    s3client = s3_client()
    paginator = s3client.get_paginator('list_objects_v2')
    for result in paginator.paginate(Bucket=bucket, Delimiter='/'):
        if result.get('CommonPrefixes') is not None:
            for subdir in result.get('CommonPrefixes'):
                parent_dir.append(subdir.get('Prefix'))

    return parent_dir
