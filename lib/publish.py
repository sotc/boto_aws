from uca import s3
from uca import dynamo
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Populate project location from S3
def user_proj_dynamo(username):
    """
    This function retrieves user information from project table in dynamoDB
    """
    logger.info("Username: %s", username)

    user_data = dynamo.query_user_projects(username)
    json_data = json.loads(user_data)
    logger.info("Users data: %s", json_data)

    project_list = [x['ProjId'] for x in json_data['Items']]

    return project_list

def s3_pub_files(username):
    """
    Retrieve a list of users files from publish bucket in S3
    """
    s3_bucket = "company-publish"
    proj_name = user_proj_dynamo(username)
    proj_files = []
    for proj in proj_name:
        s3_path = username + '/' + proj + '/'
        proj_files.append(s3.get_files(s3_bucket, s3_path))
    return proj_files

def s3_pub_dir(username):
    """
    Retrieve a list of directories from the publish s3 bucket
    """
    
    s3_bucket = "company-publish"
    proj_name = user_proj_dynamo(username)
    proj_dirs = []
    for proj in proj_name:
        s3_path = username + '/' + proj + '/'
        proj_dirs.append(s3.get_subdir(s3_bucket, s3_path))
    return proj_dirs
