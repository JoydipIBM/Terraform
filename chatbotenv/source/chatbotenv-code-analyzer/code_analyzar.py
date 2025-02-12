import boto3, os, json, re, datetime, asyncio
from uuid import uuid4
from boto3.dynamodb.conditions import Attr

class Code_analyzar:
    session = boto3.Session()
    bedrock_client = session.client('bedrock-agent-runtime')
    bedrock_runtime = boto3.client(service_name="bedrock-runtime")
    modelId = os.environ['model_id']
    temp = float(os.environ["tempreture"])
    topp = float(os.environ["topP"])
    table_name = os.environ['table_doc_status']
    application_id = os.environ["application_id"]

    def __init__ (self, record_Id, bucket=None, file_name=None):
        self.record_Id = record_Id
        self.bucket = bucket
        self.file_name = file_name
        self.content = ''
        self.summary = ''
        self.documentation = ''
        self.bestpractices = ''
        self.vulnerability = ''
        self.codetype = ''
        self.score = ''
        self.status = 'PROCESSING'
        # self.__fetch_file_content()
        self.save()
    
    def to_json(self):
        return json.dumps({
            "record_Id" : self.record_Id,
            "bucket" : self.bucket,
            "file_name" : self.file_name,
            "content" : self.content,
            "summary" : self.summary,
            "documentation" : self.documentation,
            "bestpractices" : self.bestpractices,
            "vulnerability" : self.vulnerability,
            "codetype" : self.codetype,
            "score" : self.score,
            "status" : self.status
        })
    
    def save(self):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(Code_analyzar.table_name)
        item = {
            'appcode': Code_analyzar.application_id,
            'connection_id': '',
            'filename': self.file_name,
            'record_Id': self.record_Id,
            'targetKey': self.file_name,
            'file_type': self.codetype,
            'status': self.status,
            'last_updated': datetime.datetime.now().isoformat(sep=" ", timespec="seconds")
        }
        table.put_item(Item=item)
        
    def update(self):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(Code_analyzar.table_name)

        update_item = {
            'appcode': Code_analyzar.application_id,
            'connection_id': '',
            'filename': self.file_name,
            'record_Id': self.record_Id,
            'targetKey': self.file_name,
            'file_type': self.codetype,
            'status': self.status,
            'item': self.to_json(),
            'last_updated': datetime.datetime.now().isoformat(sep=" ", timespec="seconds")
        }
        
        print('Item after update data:' + json.dumps(update_item))
        table.put_item(Item=update_item)

    @property
    def get_bucket(self):
        return self.bucket
        
    @property
    def get_file_name(self):
        return self.file_name

    @property
    def get_summary(self):
        return self.summary
    
    @property
    def get_documentation(self):
        return self.documentation
    
    @property
    def get_bestpractices(self):
        return self.bestpractices
    
    @property
    def get_vulnerability(self):
        return self.vulnerability
    
    @property
    def get_score(self):
        return self.score
    
    @property
    def get_codetype(self):
        return self.codetype
    
    @property
    def set_bucket(self, value):
        self.bucket = value
    
    @property
    def set_file_name(self, value):
        self.file_name = value

    @property
    def set_summary(self, value):
        self.summary = value
    
    @property
    def set_documentation(self, value):
        self.documentation = value
    
    @property
    def set_bestpractices(self, value):
        self.bestpractices = value
    
    @property
    def set_vulnerability(self, value):
        self.vulnerability = value
    
    @property
    def set_score(self, value):
        self.score = value 
        
    @property
    def set_codetype(self, value):
        self.codetype = value 