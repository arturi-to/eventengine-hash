## Project retreive hash for "Event Engine" events

Objective:
Improve participants experience with a simple web application where participants can retreive an Event Engine team "hash" for lab access, in a self-service manner.

AWS Services
- SQS
- DynamoDB
- Cognito

Diagram:

![application-aws-services](https://github.com/gcanales75/eventengine-hash/blob/master/readmeImages/ee-hash.png))

1. Event Engine participants makes an authentication request against an Cognito Identity Pool with enabled access to unauthenticated identities. The unauthenticated identity pool has a IAM role attached with SQS and DynamoDB permissions.
2. Cognito authenticates user
3. User request a SQS message, this would be a Event Engine team access hash
4. SQS queue returns a message from the queue
5. Application deletes retrieved SQS message
6. Application writes an item in the DynamoDB table (hash value and email)

Important note to participants: Instructor must tell participants to not to re-submmit their hash request, if they experience problems retrieving the hash must approach the instructor for help.

Web application was developed using the SDK for JavaScript in the browser

AWS SDK for JavaScript in the Browser: https://aws.amazon.com/sdk-for-browser/

### AWS Services deployment

This application consumes AWS services which are deployed with the CloudFormation template. 

AWS Services
- SQS
- DynamoDB
- Cognito
  
(Option) Instructor can updated this parameters:

- Cognito Identity Pool Name
- DynamoDB table Name
- SQS queue Name

### Load hashes file to the SQS queue

A python script file 'sendmessages.py' is included in the repo to upload the hashes file to the SQS queue

Usage instructions:

Pre-requisites:
- Local AWS CLI credentials
- boto3 installed locally
- Python 3 installed
- SQS queue URL (SQS queue deployed with the CloudFormation template)
- Hashes file downloaded from Event Engine event, file needs to be a non-formatted TXT file with no headers

Run the python script
[console] $ python3 sendmessages.py https://sqs.us-east-1.amazonaws.com/<ACCOUNT>/<SQS-queue-name> <hashes TXT file path>
e.g. $ python3 sendmessages.py https://sqs.us-east-1.amazonaws.com/123456789012/myhashmessages.fifo hashListExampleFile.txt
Important: Do not re-send file, it will duplicate hashes on SQS queue

### Application

Application and all dependencies are included in the 'website' folder of the repo

- 'index.html' file
- 'css/' folder
- 'font/' folder
- 'images/' folder
  
Instructor needs to update some variables values in the 'index.html' file based on the CloudFormation Output parameters

- Line 63 with the 'SQSqueueUrl' key output value. Description: 'SQS queue URL'
- Line 64 with the 'DynamoDbHashTable' key output value. Description: 'DynamoDB Table Name'
- Line 65 with the 'CognitoIdentityPoolId' key output value. Description: 'Cognito Identity Pool ID'

DEFAULT REGION: us-east-1
If you are deploying this project in a different region edit line 68 of 'index.html' file

### Conteinarize the application

Application can be deployed in a Docker container, repo includes a Dockerfile for that purpose

Sample commands to build an image and push it to an ECR container registry

Docker build image
docker build -t stp/ee-hash-retrieve .

Create ECR repository (requires AWS CLI session credentials)
aws ecr create-repository --repository-name stp/ee-hash-retrieve

ECR registry authentication
$(aws ecr get-login --registry-ids ${ACCOUNT_NUMBER} --no-include-email --region ${AWS_REGION})

Tag image
docker tag stp/ee-hash-retrieve:latest ${ACCOUNT_NUMBER}.dkr.ecr.${AWS_REGION}.amazonaws.com/stp/ee-hash-retrieve:latest

Push image to ECR
docker push ${ACCOUNT_NUMBER}.dkr.ecr.${AWS_REGION}.amazonaws.com/stp/ee-hash-retrieve:latest

