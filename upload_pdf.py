from boto3 import Session, client
import os
import json
import requests
import glob
import datetime

AWS_ACCESS_KEY = os.environ["AWS_ACCESS_KEY"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
SLACK_TOKEN = os.environ["SLACK_TOKEN"]
PDF_OUTPUT_DIR = os.environ.get("PDF_OUTPUT_DIR", "/docs/_build/latex/*.pdf")


session = Session(aws_access_key_id=AWS_ACCESS_KEY,
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                  region_name='ap-northeast-1')

PREFIX = 'blueprism_curriculum/'
BUCKET = 'tsh-fs-distribute'

s3resource = session.resource('s3')
bucket = s3resource.Bucket(BUCKET)

def get_presigned_url(bucket, key):
    s3_client = session.client('s3')
    url = s3_client.generate_presigned_url(
        ClientMethod = 'get_object',
        Params = {'Bucket' : bucket,
                          'Key' : key},
        ExpiresIn = 432000,
        #ExpiresIn = 2592000,
        HttpMethod = 'GET')
    return url

def send_message(target, message, *, sender_name="bot"):
    """Slack通知する"""
    END_POINT = "https://slack.com/api/chat.postMessage"
    TOKEN = SLACK_TOKEN
    headers = {"Content-type": "application/json", "Authorization": "Bearer {}".format(TOKEN)}
    requests.post(
        END_POINT,
        headers = headers,
        data = json.dumps(
            # 引数はここで使う
           {"text": message, "channel":target , "username": sender_name, "icon_emoji": ":robot_face:"}
     )
    )

if __name__ == "__main__":
    files = glob.glob(PDF_OUTPUT_DIR)
    # ログもアップロード
    files.append('/tmp/document_build.log')
    for f in files:
        key = '{}{}_{}'.format(PREFIX, str(datetime.datetime.now()), os.path.basename(f))
        bucket.upload_file(f, key)
        message = 'filename : {} \ndownload url : {} \n 有効期限は5日間です'.format(os.path.basename(f), get_presigned_url(BUCKET, key))
        send_message("org-fs-bot_ntfctn", message) 
