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

Important note to participants: Instructor must tell participants to not to re-submmit their hash request, if they experience problems retrieving the hash must approach the instructor for help. (Working in a fix for this)

Web application was developed using the SDK for JavaScript in the browser

AWS SDK for JavaScript in the Browser: https://aws.amazon.com/sdk-for-browser/

### AWS Services deployment

This application consumes AWS services which are deployed with the CloudFormation template included in this repo, inside CF-templates/

AWS Services
- SQS queue
- DynamoDB table
- Cognito identity pool
- Lambda function
  
### Deploying the App

Before creating the CloudFormation stack, instructor will need to create a S3 bucket or use an existing one, upload the ee-hash-lambda.zip file provided in this repo to the S3 bucket, and also the content of the website folder for host the App with S3.

This are the CloudFomation Parameters that would need to be provided:

- Lambda code repository S3 bucket
- Lambda zip file S3 key (e.g. ee-hash-lambda.zip)
- Cognito Identity Pool Name
- DynamoDB table Name
- SQS queue Name


### Load hashes file to the SQS queue

Download the CSV file from Event Engine event and save hashes in a TXT file unformatted with no header, use the name hash_containers_name_of_partner.txt by example hash_container_dxc.txt or hash_container_public.txt this is important next.
Before uploading the hashes TXT file bucket need to be configured to receive events notifications, such as a the hashes file upload action.

S3 bucket Event configuration using the console

1. Services -> S3
2. Click on the bucket you will use to upload the hashes TXT files
3. Click on the "Properties" tab
4. Click on events
5. Click on "+ Add notification"
6. Enter a Name (e.g. "ee-hashfile-event")
7. Mark "All object create events"
8. In Prefix put "hash", without quotes
9. In suffix put "txt", without quotes
10. Display the options in the "Send to" combo and select "Lambda Function"
11. Display the options in the "Lambda" combo and select "ee-read-hash-file-1" (This is the Lambda function created with CloudFormation)
12. Click "Save"

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

- Update line 65 with the 'SQSqueueUrl' key output value. Description: 'SQS queue URL'
- Update line 66 with the 'DynamoDbHashTable' key output value. Description: 'DynamoDB Table Name'
- Update line 67 with the 'CognitoIdentityPoolId' key output value. Description: 'Cognito Identity Pool ID'

DEFAULT REGION: ```us-east-1```
If you are deploying this project in a different region edit line 68 of 'index.html' file

### Hosting the App on S3

Application can be deployed in S3 to use a serverless option ;)

1. Services -> S3
2. Click on the bucket that you already use to host the hashes
3. Click on the "Properties" tab
4. Click on Static website hosting
5. Click on "Use this bucket to host a website"
6. Double check that the Index document is index.html
7. Click "Save"

**Tip: remember to check permissions to S3 to publish the website, you can look here --> https://docs.aws.amazon.com/AmazonS3/latest/dev/HowDoIWebsiteConfiguration.html**

Have fun!
