import logging, os, json
import urllib
from code_profiler import Code_profiler

LOGLEVEL = os.environ["logging_level"].upper()
logger = logging.getLogger()
logger.setLevel(LOGLEVEL)

def lambda_handler(event, context):
    file_info = json.loads(event['file_info'])
    print (file_info)
    try :
        profiler = Code_profiler(**file_info)
        profiler.process()
        logger.info(profiler.to_json())
        
    except Exception as e:
        error_message = str(e)
        logger.error(e)
        return {"statusCode": 500, "body": f"{error_message}"}

    return {
            'statusCode': 200,
            'response': 'done'
        }
        