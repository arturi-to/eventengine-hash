import boto3
import random
import os

queueUrl = os.environ["queueUrl"]
sqs = boto3.client('sqs')
s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    hashfile = s3.get_object(Bucket=bucket, Key=key)
    lines = hashfile['Body'].read().split(b'\n')
    
    for hash in lines:
        dedupeId = random.choice(range(1000001, 9999999))
        response = sqs.send_message(
            QueueUrl=queueUrl,
            MessageBody=hash.decode(),
            MessageDeduplicationId= str(dedupeId),
            MessageGroupId='eeHashGroupId'
        )