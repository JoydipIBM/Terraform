import boto3, os, json, re, datetime, asyncio
from uuid import uuid4
from boto3.dynamodb.conditions import Attr

class Code_profiler:
    session = boto3.Session()
    bedrock_client = session.client('bedrock-agent-runtime')
    bedrock_runtime = boto3.client(service_name="bedrock-runtime")
    modelId = os.environ['model_id']
    temp = float(os.environ["tempreture"])
    topp = float(os.environ["topP"])
    topk = int(os.environ["topK"])
    max_tokens = int(os.environ["maxTokenCount"])
    anthropic_version = os.environ['anthropic_version']
    role = os.environ['role']
    table_name = os.environ['table_doc_status']

    application_id = os.environ["application_id"]

    def __init__ (self, bucket=None, file_name=None, **kwargs):
        self.bucket = bucket
        self.file_name = file_name
        for key in kwargs:
            setattr(self, key, kwargs[key])
        self.__fetch_file_content()
    
    
    def __execute(self, content=None):
        body = json.dumps({
            "anthropic_version": Code_profiler.anthropic_version,
            "max_tokens":Code_profiler.max_tokens,
            "messages":[
                {
                    "role": Code_profiler.role,
                    "content": [{ "type": "text", "text": content}]
                }],
                "temperature": Code_profiler.temp,
                "top_p": Code_profiler.topp,
                "top_k": Code_profiler.topk
        })
        response =  Code_profiler.bedrock_runtime.invoke_model(
            body=body,
            modelId=Code_profiler.modelId,
            accept="application/json", 
            contentType="application/json"
        )  
        streaming_body = response.get('body')
        body_str = streaming_body.read().decode('utf-8')
        return json.loads(body_str)

    def __fetch_file_content(self):
        s3 = boto3.client('s3')
        response = s3.get_object(Bucket=self.bucket, Key=self.file_name)
        self.content = response['Body'].read().decode('utf-8')
    
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
            "status" : self.status,
            "testcase" : self.testcase,
            "testcode" : self.testcode
        })
    
    def process(self):
        # content =self.content +  "Generate the summary of the below code within <summary> tag. generate the documentation of the code within <documentation> tag. Scan the code and suggest whether best practices followed within <bestpractices> tag and if any vulnerability exists within <vulnerability> tag. Also give me the code type of the below code within <codetype> tag."
        #content = self.content + 'Generate the summary of the above code within <summary> tag. generate the documentation of the code within <documentation> tag. Scan the code and suggest whether best practices followed within <bestpractices> tag and if any vulnerability exists within <vulnerability> tag. Also give me the code language of the below code within <code_language> tag. give me the numaric score between 0 to 100 within <score> tag based on the bestpractices show score only in percentage <score_percentage> from score. detect language in <language> from code_language'
        
        # prompt = f'''
        #             You are very good code analyzer, a code snipped is provided within the tag <code></code>. You need to analyze the code in the following manner:
        #             1. Summarize the code so that an user can understand what the code flow dose and the functionality of the code.
        #             2. Documentation of the code to understand the steps on the code flow.
        #             3. Analyze the code for adherence to best practices. Identify any instances where best practices are not followed, referencing the specific parts of the provided code. For each identified issue, suggest the correct best practice and indicate which part of the code should be modified to comply with it. Present your findings in JSON format, with each vulnerability represented as an object containing the keys: "issue", "suggestion", "code" and "location".
        #             4. Conduct a security analysis of the provided code snippet to identify potential vulnerabilities. For each vulnerability found: "Provide a name for the vulnerability", "Explain the vulnerability and its potential impact", "Indicate where in the code the vulnerability exists with existing code refernce and line number", "Suggest methods to mitigate or resolve the vulnerability". Present your findings in JSON format, with each vulnerability represented as an object containing the keys: "name", "description", "location", and "mitigation".
        #             5. What the coding language ?
        #             6. Understanding the coding language generate the test case for the provided code snipped
        #             7. Understanding the coding language generate the test code to run the test case for the provided code snipped.
        #             8. give me the numeric score between 0 to 100 based on the best practices.
        #             Put the above 8 points output in the a json format where json key name will be summary, documentation, bestpractice, vulnerability, codinglanguage, testcase, testcode and score respectively.
        #             <code>{self.content}</code>'''
        
        prompt = f'''As an expert code analyzer, you'll examine a code snippet enclosed in <code></code> tags. Your analysis should include:
                    
                    1. A user-friendly summary of the code's functionality and flow.
                    
                    2. Step-by-step documentation of the code's execution process.
                    
                    3. Best practices evaluation:
                       - Identify deviations from best practices
                       - Pinpoint its location in the code (with line numbers)
                       - Suggest improvements
                       - Present findings in JSON format with keys: "issue", "suggestion", "code", and "location"
                    
                    4. Security vulnerability assessment:
                       - Name each vulnerability
                       - Explain its potential impact
                       - Pinpoint its location in the code (with line numbers)
                       - Propose mitigation strategies
                       - Present findings in JSON format with keys: "name", "description", "location", and "mitigation"
                    
                    5. Identify the programming language used.
                    
                    6. Generate appropriate test cases for the code snippet.

                    7. Provide test code to execute the generated test cases.
                    
                    8. Assign a numerical score (0-100) based on adherence to best practices.
                    
                    Put the above 8 points output in the a json format where json key name will be summary, documentation, bestpractice, vulnerability, codinglanguage, testcase, testcode and score respectively.
                    <code>{self.content}</code>'''
        
                    
        stream_dict = self.__execute(prompt)
        output_text = json.loads(stream_dict['content'][0]['text'], strict=False)
        input_tokens = stream_dict['usage']['input_tokens']
        output_tokens = stream_dict['usage']['output_tokens']
        
        if "summary" in output_text:
            self.summary = output_text["summary"]
            print('summary : ' + self.summary)
        if "documentation" in output_text:
            self.documentation = output_text["documentation"]
            print('documentation : ' + self.documentation)
        if "bestpractice" in output_text:
            self.bestpractices = str(output_text["bestpractice"])
            print('bestpractices : ' + self.bestpractices)
        if "vulnerability" in output_text:
            self.vulnerability = str(output_text["vulnerability"])
            print('vulnerability : ' + self.vulnerability)
        if "testcase" in output_text:
            self.testcase = str(output_text["testcase"])
            print('testcase : ' + self.testcase)
        if "testcode" in output_text:
            self.testcode = str(output_text["testcode"])
            print('testcode : ' + self.testcode)
        if "codinglanguage" in output_text:
            self.codetype = output_text["codinglanguage"]
            print('codetype  : ' + self.codetype)
        if "score" in output_text:
            self.score = output_text["score"]
            print('score_percentage : ' +  str(self.score) + '%')
            print('score : ' + str(self.score))
        self.status = 'COMPLETED'
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
        
        self.update()
    
    def save(self):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(Code_profiler.table_name)
        item = {
            'appcode': Code_profiler.application_id,
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
        table = dynamodb.Table(Code_profiler.table_name)
        result = table.scan(FilterExpression=  Attr('record_Id').eq(self.record_Id))
        item = result['Items'][0] if (len(result['Items']) > 0) else result['Items']
        analysis = json.loads(self.to_json())
        
        del analysis['content']
        
        item_tobe_updated = {
            'appcode': Code_profiler.application_id,
            'filename': item['filename'],
            'connection_id': item['connection_id'],
            'file_type': self.codetype,
            'record_Id': item['record_Id'],
            'targetKey': item['targetKey'],
            'status': self.status,
            'analysis': json.dumps(analysis),
            'last_updated': datetime.datetime.now().isoformat(sep=" ", timespec="seconds"),
            'summary': self.summary,
            'documentation': self.documentation,
            'bestpractices': self.bestpractices,
            'vulnerability': self.vulnerability,
            'testcase': self.testcase,
            'testcode': self.testcode,
            'score': self.score,
            'input_tokens': self.input_tokens,
            'output_tokens': self.output_tokens
        }
        
        table.put_item(Item=item_tobe_updated)

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