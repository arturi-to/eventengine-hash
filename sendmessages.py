######
# Script usage
# Hash file must be a TXT formatted file
#
# $ python3 sendmessages.py https://sqs.us-east-1.amazonaws.com/<ACCOUNT>/<SQS-queue-name> <hashes TXT file path>
#
# e.g. $ python3 sendmessages.py https://sqs.us-east-1.amazonaws.com/123456789012/myhashmessages.fifo hashListExampleFile.txt
#
# Important: Do not re-send file, it will duplicate hashes on SQS queue
#
# Author: gilberto canales <glcnl@amazon.com>
######

import boto3
import random
import os
import time
import sys

client = boto3.client('sqs')
queueUrl = sys.argv[1]
hashTxtFile = sys.argv[2]

with open(hashTxtFile, 'r') as file:
    for hash in file:
        dedupeId = random.choice(range(1000001, 9999999))
        response = client.send_message(
            QueueUrl=queueUrl,
            MessageBody=hash,
            MessageDeduplicationId= str(dedupeId),
            MessageGroupId='eeHashGroupId'
        )
num_lines = sum(1 for line in open('hashList.txt'))
print('Succesfully sent ' + str(num_lines) + ' hashes to SQS queue!')