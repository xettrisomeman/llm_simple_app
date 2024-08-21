import os
from cohere.client import Client
from dotenv import load_dotenv
from llms import AnthropicClass, CohereClass

load_dotenv()

api_key = os.environ["COHERE_API_KEY"]

 
client = Client(
            api_key=api_key,
        )
models = client.models.list().models

for model in models:
    if "chat" in model.endpoints:
        print(model.name)



