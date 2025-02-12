import boto3
import json
from botocore.exceptions import ClientError





class Premier:
    def __init__(self, bedrockKnowledgeBaseId, overrideSearchType="HYBRID", maxResultCount = 1, temperature = 0, topP = 0.9):
        self.bedrockKnowledgeBaseId = bedrockKnowledgeBaseId
        self.maxResultCount = maxResultCount
        self.temperature = temperature
        self.topP = topP
        self.searchResultSources = {}
        self.overrideSearchType = overrideSearchType
        self.modelId="amazon.titan-text-premier-v1:0"
        self.inputToken = 0
        self.outputToken = 0
        self.result = None
        self.resultText = ""

    def LookupVectorDB(self, query):
        bedrock_client = boto3.client('bedrock-runtime')
        bedrock_agent_client = boto3.client("bedrock-agent-runtime")

        response = bedrock_agent_client.retrieve(
            retrievalQuery= {
                'text': query
            },
            knowledgeBaseId=self.bedrockKnowledgeBaseId,
            retrievalConfiguration= {
                'vectorSearchConfiguration': {
                    'numberOfResults': self.maxResultCount,
                    #'overrideSearchType': self.overrideSearchType # optional
                }
            }
        )
        
        results = response['retrievalResults']
        for result in results:
            #print(result)
            try:
                uri = result['location']['s3Location']['uri']
                content = result['content']['text']
                if uri in self.searchResultSources:
                    self.searchResultSources[uri].append(content)
                else:
                    self.searchResultSources[uri] = [content]
            except TypeError as e:
                print(f"TypeError encountered: {e}")
                continue
            except KeyError as e:
                print(f"KeyError encountered: Missing key {e}")
                continue
        
        try:
            json_output = json.dumps(self.searchResultSources, indent=4)
            return json_output
        except TypeError as e:
            print(f"TypeError during JSON serialization: {e}")

        
    def Search(self, prompt):
        bedrock_client = boto3.client('bedrock-runtime')
        all_texts = ""
        
        lookupvalue = self.LookupVectorDB(prompt)
        references = json.loads(lookupvalue)
        
        print("look up value",lookupvalue)
        
        for filename, texts in references.items():
            for text in texts:
                all_texts += f"{text} \n"

        instruction = """
                INSTRUCTIONS: \n\n
                - You are an AI assistant specifically designed to provide responses based solely on the provided references.
                - Between <QUERY></QUERY> tags, a prompt/question will be provided which you need to respond to.
                - Between <REFERENCES></REFERENCES> tags, you will be provided a set of text chunks from different documents which you must use to form your response.
                - The chunks will be provided in a JSON format, which will also contain the file path from where each chunk has been taken.
                - A single file can have multiple text chunks referred to.
                - Your response must be derived using only the information available in the <REFERENCES> block.
                - Do not speculate, predict, or use any external context or references to formulate your answer beyond what has been provided in the <REFERENCES> block.
                - If sufficient information is not available in the provided <REFERENCES>, then decline to answer, stating that the information is not available.
                - Organize your responses clearly with appropriate formatting and structure.
                -  step-by-step before answering, basing your reasoning solely on the provided references.
                - Stay neutral and factual on sensitive topics, avoiding any personal opinions or biases.
                - Use concise sentences and break up long paragraphs for better readability.
                - Avoid using flowery language, abbreviations, or jargon unless they are present in the provided references.
                - The response should be in JSON format with the following fields:
                - "Answer": The answer to the query, derived strictly from the provided references.
                  - "Query": The query that was asked.
                  - "Context": An array of references used to generate the answer, with each reference having the following elements:
                    - "File_name": The file name from where the chunk(s) has been taken.
                    - "Refered_text": An array containing the text chunk(s) that have been referred to from the file.
                \n\n
                REFERENCES: \n\n
                {search_results}
                \n\n
                QUERY:\n\n
                {question}
                \n\n
                RESPONSES:
                """.format(question=prompt,search_results=lookupvalue)
                
        print(instruction)
        
        body = json.dumps({
            "inputText": instruction, 
            "textGenerationConfig":{  
                "temperature":self.temperature, #Temperature controls randomness; higher values increase diversity, lower values boost predictability.
                "topP":self.topP # Top P is a text generation technique, sampling from the most probable tokens in a distribution.
            }
        })
        
        response = bedrock_client.invoke_model(
            body=body,
        	modelId=self.modelId,
            accept="application/json", 
            contentType="application/json"
        )
        
        streaming_body = response['body']

        # Read the StreamingBody object into a string
        body_str = streaming_body.read().decode('utf-8')
        
        stream_dict = json.loads(body_str)
        
        self.inputToken = stream_dict['inputTextTokenCount']
        self.result = stream_dict['results']
        self.outputToken = self.result[0]['tokenCount']
        self.resultText = self.result[0]['outputText']
        
        print(self.resultText)
