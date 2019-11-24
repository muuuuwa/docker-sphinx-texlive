import boto3
import os
import json
from urllib.parse import unquote, parse_qs


AWS_ACCESS_KEY = os.environ["MY_AWS_ACCESS_KEY"]
AWS_SECRET_ACCESS_KEY = os.environ["MY_AWS_SECRET_ACCESS_KEY"]
SLACK_TOKEN = os.environ["SLACK_TOKEN"]
REPO_URL = os.environ["REPO_URL"]

def run_task(branch='master'):
    client = boto3.client("ecs")
    res = client.run_task(
        cluster="default",
        taskDefinition="blueprism-pdf-build:1",
        overrides={
            "containerOverrides": [{
                "name": "sphinx-texlive",
                "environment": [
                    {"name": "AWS_ACCESS_KEY", "value": AWS_ACCESS_KEY},
                    {"name": "AWS_SECRET_ACCESS_KEY", "value":  AWS_SECRET_ACCESS_KEY},
                    {"name": "SLACK_TOKEN", "value":  SLACK_TOKEN},
                    {"name": "REPO_URL", "value":  REPO_URL},
                    {"name": "BRANCH", "value":  branch},
                ]
            },],
            'executionRoleArn': 'arn:aws:iam::036823603385:role/ecsTaskExecutionRole',
        },
        count=1,
        launchType='FARGATE',
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': [
                    'subnet-090c7e47e26e91758', # replace with your public subnet or a private with NAT
                ],
                'assignPublicIp': 'ENABLED'
            }
        }
    )
    return str(res)


def lambda_handler(event, context):
    body = event['body']
    unquoted_body = unquote(body)
    parsed_body = parse_qs(unquoted_body)
    payload_str = parsed_body['payload'][0]
    payload = json.loads(payload_str)
    ref = payload['ref']
    ref_part = ref.split('/')[-1]
    
    res = {
            "statusCode": 200,
            #"body" : "ref : {}".format(ref_part)}
            "body": run_task(branch=ref_part)}
    return res


if __name__ == "__main__":
    run_task(branch='pxchfon')
