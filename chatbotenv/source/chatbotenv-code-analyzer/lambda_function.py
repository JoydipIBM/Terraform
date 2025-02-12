import logging, os, json, shutil
import urllib.parse, boto3, zipfile
from uuid import uuid4
from code_analyzar import Code_analyzar

LOGLEVEL = os.environ["logging_level"].upper()
logger = logging.getLogger()
logger.setLevel(LOGLEVEL)

def unzip_and_upload(zip_file_path, bucket_name, extraction_dir='/tmp/extracted_files'):
   
    os.makedirs(extraction_dir, exist_ok=True)

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extraction_dir)
        
    s3 = boto3.client('s3')

    for root, dirs, files in os.walk(extraction_dir):
        for file in files:
            file_path = os.path.join(root, file)
            s3_key = os.path.relpath(file_path, extraction_dir)
            try:
                s3.upload_file(file_path, bucket_name, s3_key)
                logger.info(f'Successfully uploaded {s3_key} to {bucket_name}')
            except Exception as e:
                print(e)

    shutil.rmtree(extraction_dir)

def lambda_handler(event, context):
    try:
        logger.info(event)
        logger.info("Generating response")
        requestId = context.aws_request_id

        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
        logger.info(bucket)
        logger.info(key)
        extension = os.path.splitext(key)[1]
        logger.info(f"File extension: {extension}")

        if extension == ".zip":
            s3 = boto3.client('s3')
            zip_file_path = f'/tmp/{os.path.basename(key)}'
            s3.download_file(bucket, key, zip_file_path)

            unzip_and_upload(zip_file_path, bucket)
        else:
            #code validation will be place here and call another lambda to process the code for profiling
            file_analyzer = Code_analyzar(record_Id=str(uuid4()), bucket=bucket, file_name=key)
    
            client = boto3.client('lambda')
            inputParams = {
                "file_info": file_analyzer.to_json()
            }
            response = client.invoke(
                FunctionName=os.environ["insightx_code_profiler_fn_name"],
                InvocationType='RequestResponse',
                Payload=json.dumps(inputParams)
            )
            
            print(inputParams)
            
    except Exception as e:
        error_message = str(e)
        logger.error(e)
        return {"statusCode": 500, "body": f"{error_message}"}
    
    return {
        'statusCode': 200
    }
