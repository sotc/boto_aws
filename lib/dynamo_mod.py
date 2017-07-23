"""Library For Interacting with DynamoDB

DynamoDB Tables:

"""
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import (Attr, Key)
from sensible.loginit import logger
from random import random
import json

import time

log = logger(__name__)
REGION = 'us-west-2'


def dynamo_client():

    log_dynamo_client_msg = "Creating DynamoDB CLIENT connection in Region: [%s]" % REGION
    client = boto3.client('dynamodb', region_name=REGION)
    log.info(log_dynamo_client_msg)
    return client

def dynamo_resource():

    log_dynamo_resource_msg = "Creating DynamoDB RESOURCE connection in Region: [%s]" % REGION
    resource = boto3.resource('dynamodb', region_name=REGION)
    log.info(log_dynamo_resource_msg)
    return resource


###Project Methods
def random_project_name(qprefix = "Proj"):
    """Generates a randome name for a project.
    This will need to be a module at some point
    """

    num = int(round(1000000000 * random()))
    project_name_integration = "%s-%s" % (qprefix, num)
    return project_name_integration


def create_project(dictargs):
    """Creates Project Table Record That Links With Group Name
    projectName, userId, username
    proj = create_project("testProject", "TestCompany")
    """

    db = dynamo_resource()
    dbt = db.Table("Projects")

    #projId = random_project_name(qprefix=projectName)

    try:
        res = dbt.put_item(
        Item={
            'UserId': dictargs['username'],
            'ProjId': dictargs['projname'],
        },
        # Use ConditionalExpression to make sure project does not already exist
        ConditionExpression='attribute_not_exists(ProjId)'
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            message = "projname=%s already exists for username=%s" % \
                    (dictargs['projname'], dictargs['username'])
            return {'error_code': e.response['Error']['Code'],
                    'status_code': 409,
                    'message': message}
        else:
            db_log_msg = "Added to UserProjects Table with [%s]" % res
            return {'response': res,
                    'status_code': 200,
                    'message': "SUCCESS: %s" % (db_log_msg)}


    db_log_msg = "Added to UserProjects Table with [%s]" % res
    log.info(db_log_msg)

    return {'response': res,
            'status_code': 200,
            'message': "SUCCESS: %s" % (db_log_msg)}


def update_project_record(dictargs):
    """
    Update Item with lastStatus information.

    lastStatus = tuple or list with two elemenst taskname, status)
    """

    db = dynamo_resource()
    dyn_table = db.Table("Projects")

    res = dyn_table.update_item(
    Key={
        'UserId': dictargs['username'],
        'ProjId': dictargs['projname'],
        'TaskName': dictargs['taskname'],
        'TaskStatus' : dictargs['taskstatus'],
    },
    UpdateExpression="set TaskStatus = :ls",
    ExpressionAttributeValues={
        ':ls': dictargs['taskstatus']
    },
    ReturnValues="UPDATED_NEW"
    )
    db_log_msg = "Updated TaskStatus information with [%s]" % res
    log.info(db_log_msg)
    return res

def delete_user_project(payload):
    """Deletes project record from the UserProjects Table
    """

    userId = payload['username']
    projectId = payload['projname']

    db = dynamo_resource()
    dyn_table = db.Table("Projects")
    print userId
    print projectId
    try:

        res = dyn_table.delete_item(
            Key={
            'UserId': userId,
            'ProjId': projectId
            },
            ConditionExpression="ProjId = :val",
            ExpressionAttributeValues= {
                ":val": projectId
                }
        )
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            db_log_msg = e.response['Error']['Message']
            log.info(db_log_msg)
        else:
            raise
    else:
        db_log_msg = "DeleteItem succeeded: %s %s" % (userId, projectId)
        log.info(db_log_msg)
        return res

def get_project_item(userId, projId):
    """List the projects associated with user
    Need to add json to return item
    """

    db = dynamo_resource()
    dyn_table = db.Table("Projects")

    res = dyn_table.get_item(
        Key={
            'UserId': userId,
            'ProjId': projId
        }
    )
    try:
        item = res['Item']
    except KeyError:
        msg = "No items in control record for: %s, %s" % userId, projId
        log.exception(msg)
        item = None
    return item

def query_user_projects(userId):
    """Query projects by userID for attribute
    """

    db = dynamo_resource()
    dyn_table = db.Table("Projects")

    res = dyn_table.query(
        KeyConditionExpression=Key('UserId').eq(userId)
    )

    db_log_msg = "Query table by userId [%s]" % res
    log.info(db_log_msg)
    res = json.dumps(res)
    return res
