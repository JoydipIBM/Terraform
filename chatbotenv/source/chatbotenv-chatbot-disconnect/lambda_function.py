
import os
import logging
import json
import datetime

def lambda_handler(event, context):
    
    connectionId = event["requestContext"]["connectionId"]
    requestId = event["requestContext"]["requestId"]
    eventType = event["requestContext"]["eventType"]

    logger = logging.getLogger()
    logger.setLevel("INFO")
    
    logger_params = {
            "connectionId": connectionId,
            "log_metrix_type":"CHATBOT_DISCONNECT_REQUEST",
            "eventType" : eventType,
            "requestId": requestId,
            "disconnect_timestamp" : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    logger.info(event,extra= logger_params)

    return {
        'statusCode': 200,
        'body': json.dumps("Hello World!")
    }