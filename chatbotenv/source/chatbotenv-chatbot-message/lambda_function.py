import json
import os
import boto3
import logging
from uuid import uuid4
import datetime
from botocore.exceptions import ClientError

from completion import Completion
from completion import Response
from completion import Context

LOGLEVEL = os.environ["logging_level"].upper()
logger = logging.getLogger()
logger.setLevel(LOGLEVEL)


def generate_response(question, knowledgebase_results=None) -> Completion:
    
    temp = float(os.environ["tempreture"])
    topp = float(os.environ["topP"])
    #anthropic_version = os.environ['anthropic_version']
    max_tokens = int(os.environ["maxTokenCount"])
    #role = os.environ['role']
    topk = int(os.environ["topK"])
    
    # user_prompt = '''
    #     # Instruction #
    #     You are a advisor to the human who will provide prompts and you need to generate comprehensive response by taking additional information into account  
    #     ###################
        
    #     # Human #
    #     {question}
    #     ###################
        
    #     # Information #
    #     {knowledgebase_results}
    #     '''.format(question=question, knowledgebase_results=knowledgebase_results)
    
    system_prompt = '''You are an advanced AI assistant specialized in analyzing and reviewing computer programming languages. Your primary functions include:
                        
                        1. Code Analysis:
                            - Examine code snippets for efficiency, readability, and best practices
                            - Identify potential bugs, security vulnerabilities, and performance issues
                            - Suggest optimizations and improvements
                     
                        2. Language Comparison:
                            - Compare features, syntax, and capabilities of different programming languages
                            - Provide insights on language strengths, weaknesses, and use cases
                         
                        3. Best Practices:
                            - Offer guidance on coding standards and conventions for various languages
                            - Recommend design patterns and architectural approaches
                         
                        4. Performance Evaluation:
                            - Assess code performance and suggest optimizations
                            - Discuss time and space complexity of algorithms
                         
                        5. Trend Analysis:
                            - Provide insights on current and emerging trends in programming languages
                            - Discuss language popularity, job market demand, and community support
                         
                        6. Learning Resources:
                            - Recommend books, courses, and online resources for learning programming languages
                            - Suggest coding exercises and projects for skill improvement
                         
                        7. Tool Recommendations:
                            - Advise on IDEs, libraries, frameworks, and tools for different languages
 
                        8. Code Generation:
                            - Generate sample code snippets to illustrate concepts or solve specific problems
                            - Refactor existing code for improved quality and maintainability
                         
                        9. Debugging Assistance:
                            - Help identify and resolve common programming errors and exceptions
                         
                        10. Version Control:
                            - Provide guidance on using version control systems (e.g., Git) effectively
                     
                        When responding to queries:
                            - Provide clear, concise explanations with code examples when appropriate
                            - Consider the user's skill level (beginner, intermediate, advanced) when explaining concepts
                            - Cite authoritative sources or official documentation when discussing language features or best practices
                            - Be objective when comparing languages, acknowledging that different languages have different strengths and use cases
                            - Encourage good coding practices, including writing clean, maintainable, and well-documented code
                         
                        You are knowledgeable about a wide range of programming languages, including but not limited to:
                        C, Python, JavaScript, Java, C++, C#, Ruby, Go, Rust, Swift, Kotlin, PHP, TypeScript, Scala, and R.
                         
                        Respond to user queries accurately and helpfully, always striving to provide the most relevant and up-to-date information about programming languages and software development practices.'''
         
    
    inference_config = {"temperature": temp, "topP": topp, "maxTokens": max_tokens}
    additional_model_fields = {"top_k": topk}
    
    logger.info(f"Generating response with model: {modelId}")
    
    logger.info(f"Here is the user prompt: {question}")
    
    response = bedrock_runtime.converse(
        modelId=modelId,
        messages= [{"role": "user","content": [{"text": question}]}],
        system=[{"text": system_prompt}],
        inferenceConfig=inference_config,
        additionalModelRequestFields=additional_model_fields
        )
    
    # try:
    #     response = bedrock_runtime.converse(
    #         modelId=modelId,
    #         messages= [{"role": "user","content": [{"text": question}]}],
    #         system=[{"text": system_prompt}],
    #         inferenceConfig=inference_config,
    #         additionalModelRequestFields=additional_model_fields
    #         )
    # except ClientError as err:
    #     message = err.response['Error']['Message']
    #     logger.error("A client error occurred: %s", message)
    #     logger.info(f"A client error occured: {message}")

    # Read the StreamingBody object into a string
    stream_dict = response
    logger.info(f"Here is the response from LLM: {stream_dict}")
    
    # Extract values into separate variables
    output_text = stream_dict['output']['message']['content']
    input_token_count = stream_dict['usage']['inputTokens']
    output_token_count = stream_dict['usage']['outputTokens']

    return Response(input_token_count,output_token_count,output_text)
    
    
    
    

endpoint_url = os.environ["api_gateway_mgmt_url"]
modelId=os.environ['model_id']

logger.info(f"endpoint_url: {endpoint_url}")
logger.info(f"modelId: {modelId}")

api_client = boto3.client("apigatewaymanagementapi",endpoint_url=endpoint_url)
# Create a session and an AmazonBedrock client
session = boto3.Session()
bedrock_client = session.client('bedrock-agent-runtime')
bedrock_runtime = boto3.client(service_name="bedrock-runtime")


def lambda_handler(event, context):
    connectionId = event["requestContext"]["connectionId"]
    
    connected_epoch_time = event["requestContext"]["connectedAt"]
    c_s, c_ms = divmod(connected_epoch_time,1000)
    connected_formatted_time = datetime.datetime.fromtimestamp(c_s, datetime.timezone.utc)

    requestId = event["requestContext"]["requestId"]
    

    try:
        body=json.loads(event["body"])
        prompt = body["prompt"]
        #application id is needed for the application specific search
        #applicationId = body["applicationId"]
        request_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        logger_params = {
            "connectionId": connectionId,
            "connect_timestamp" : connected_formatted_time.strftime("%Y-%m-%d %H:%M:%S"),
            "requestId": requestId,
            "log_metrix_type":"CHATBOT_MESSAGE_REQUEST",
            "request_timestamp" : request_timestamp,
            "prompt" : prompt,
            "applicationId" : None,
            "status": "PENDING"
        }
        logger.info("CHATBOT_MESSAGE_REQUEST",extra= logger_params)

        logger.info("Generating response")
        completion = Completion(connectionId)
        completion.response = generate_response(prompt, None)
        
        intoken = completion.response.InToken
        outtoken = completion.response.OutToken
        response_text = completion.response.OutputText 
        
        logger.info("CHATBOT_MESSAGE_RESPONSE",extra= logger_params)

        #response = api_client.post_to_connection(ConnectionId=connectionId,Data=completion)
        response = api_client.post_to_connection(ConnectionId=connectionId,Data=json.dumps(completion.to_json).encode('utf-8'))
        
        return {
            'statusCode': 200,
            'body': json.dumps(completion.to_json).encode('utf-8')
        }
    except Exception as e:
        logger_params = {
            "connectionId": connectionId,
            "log_metrix_type":"CHATBOT_MESSAGE_ERROR",
            "status" : "ERROR",
            "error_message": e
        }
        logger.error(e,extra=logger_params)
        return {"statusCode": 500, "body": f"{e}"}
    