## Self-service application to retrieve hashes in Event Engine trainings [AWS internal]

Objective:
Improve participants experience with a simple web application where participants can retreive an Event Engine team "hash" for lab access, in a self-service manner.

AWS Services
- SQS
- DynamoDB
- Cognito

Diagram:

![application-aws-services](https://github.com/gcanales75/eventengine-hash/blob/master/readmeImages/ee-hash.png)

1. Event Engine participants makes an authentication request against an Cognito Identity Pool with enabled access to unauthenticated identities. The unauthenticated identity pool has a IAM role attached with SQS and DynamoDB permissions.
2. Cognito authenticates user
3. User polls a SQS message, this would be a Event Engine team access hash
4. SQS queue returns a message from the queue
5. Application deletes SQS message
6. Application writes an item in the DynamoDB table (hash value and email)

Important note to participants: Instructor must tell participants to not to re-submmit their hash request, if they experience problems retrieving the hash must approach the instructor for help.

Web application was developed using the SDK for JavaScript in the browser

AWS SDK for JavaScript in the Browser: https://aws.amazon.com/sdk-for-browser/

### AWS Services deployment

This application consumes AWS services which are deployed with the CloudFormation template included in this repo, inside CF-templates/

AWS Services
- SQS queue
- DynamoDB table
- Cognito identity pool
- Lambda function
  
Before creating the CloudFormation stack, instructor will need to upload the lambda.zip file provided in this repo to a S3 bucket, it could be a pre-existant bucket or a new one created for this project.

This are the CloudFomation Parameters that would need to be provided:

- Lambda code repository S3 bucket
- Lambda zip file S3 key (e.g. lambda.zip)
- Cognito Identity Pool Name
- DynamoDB table Name
- SQS queue Name


### Load hashes file to the SQS queue

Download the CSV file from Event Engine event and save hashes in a TXT file unformatted with no header.
Instructor could use the same S3 bucket used to store the lambda code zip file to upload the TXT hashes file.
Before uploading the hashes TXT file bucket need to be configured to receive events notifications, such as a the hashes file upload action.

S3 bucket Event configuration using the console

1. Services -> S3
2. Click on the bucket you will use to upload the hashes TXT files
3. Click on the "Properties" tab
4. Click on events
5. Click on "+ Add notification"
6. Enter a Name (e.g. "ee-hashfile-event")
7. Mark "All object create events"
8. Display the options in the "Send to" combo and select "Lambda Function"
9. Display the options in the "Lambda" combo and select "ee-read-hash-file-1" (This is the Lambda function created with CloudFormation)
10. Click "Save"

Now instructor can upload the hashes TXT file to the S3 bucket

Important: Do not re-send file, it will duplicate hashes on SQS queue

Upload hashes file workflow diagram: 

![upload-hashes-s3](https://github.com/gcanales75/eventengine-hash/blob/master/readmeImages/ee-hash-instructor.png)

### Application

Application and all dependencies are included in the 'website' folder of the repo

- 'index.html' file
- 'css/' folder
- 'font/' folder
- 'images/' folder
  
Instructor needs to update some variables values in the 'index.html' file based on the CloudFormation Output parameters:

- Update line 63 with the 'SQSqueueUrl' key output value. Description: 'SQS queue URL'
- Update line 64 with the 'DynamoDbHashTable' key output value. Description: 'DynamoDB Table Name'
- Update line 65 with the 'CognitoIdentityPoolId' key output value. Description: 'Cognito Identity Pool ID'

DEFAULT REGION: ```us-east-1```
If you are deploying this project in a different region edit line 68 of 'index.html' file

### Conteinarize the application

Application can be deployed in a Docker container, repo includes a Dockerfile for that purpose

Sample commands to build an image and push it to an ECR container registry

Docker build image
```
docker build -t stp/ee-hash-retrieve .
```
Create ECR repository (requires AWS CLI session credentials)
```
aws ecr create-repository --repository-name stp/ee-hash-retrieve
```
ECR registry authentication
```
$(aws ecr get-login --registry-ids ${ACCOUNT_NUMBER} --no-include-email --region ${AWS_REGION})
```
Tag image
```
docker tag stp/ee-hash-retrieve:latest ${ACCOUNT_NUMBER}.dkr.ecr.${AWS_REGION}.amazonaws.com/stp/ee-hash-retrieve:latest
```
Push image to ECR
```
docker push ${ACCOUNT_NUMBER}.dkr.ecr.${AWS_REGION}.amazonaws.com/stp/ee-hash-retrieve:latest
```

Have fun!
