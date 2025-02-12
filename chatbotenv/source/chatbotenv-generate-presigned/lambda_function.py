import os
import logging
import json
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info(event)
    
    file_name = event.get("queryStringParameters").get("filename")
    bucket_name = os.environ["s3_code_submission_bucket"]
    logger.info(file_name)
    logger.info(bucket_name)
    
    try:
        if event and bucket_name:
            s3 = boto3.client("s3")
            response = s3.generate_presigned_post(
                Bucket=bucket_name,
                Key=f"{file_name}",
                # Fields={"Content-Type": "application/pdf"},
                Fields={"Content-Type": "application/octet-stream"},
                Conditions=[
                    ["starts-with", "$Content-Type", "application/"],
                    # ["content-length-range", 0, 104857699999999999],
                ],
                ExpiresIn=3600,
            )
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json",
                    'Access-Control-Allow-Origin': '*'},
                "body": json.dumps(response),
            }
    
    except Exception as e:
        logger.error(e)
        return {"statusCode": 500, "body": json.dumps("Error processing the request!")}
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json",
            'Access-Control-Allow-Origin': '*'
        },
        "body": json.dumps("Hello world!"),
    }