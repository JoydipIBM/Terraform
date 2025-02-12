import json

class Response:
    def __init__ (self, inputToken, outToken, text):
        self.inputTextTokenCount = inputToken
        self.tokenCount = outToken
        self.output_text = text
        
    @property
    def InToken(self):
        return self.inputTextTokenCount
        
    @property
    def OutToken(self):
        return self.tokenCount
    
    @property
    def OutputText(self):
        return self.output_text
        
class Context:
    def __init__(self, text, location):
        self.text = text
        self.s3_location = location

class Completion:
    def __init__(self, sessionId):
        self.connectionId = sessionId
        self.contexts = []
        self.response = None

    @property
    def context_text(self):
        return '\n'.join(context.text for context in self.contexts)

    @property
    def to_json(self):
        return json.dumps({
            "connectionId": self.connectionId,
            "contexts": [
                {"text": context.text, "s3_location": context.s3_location}
                for context in self.contexts
            ],
            "response": {
                "inputTextTokenCount": self.response.inputTextTokenCount,
                "tokenCount": self.response.tokenCount,
                "output_text": self.response.output_text
            } if self.response else None
        })
