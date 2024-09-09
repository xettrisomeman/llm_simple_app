from abc import ABC
from typing import get_args
import streamlit as st
from components.app_interface.configmanager import config

import anthropic
from langchain_anthropic import ChatAnthropic


from langchain_cohere import ChatCohere
from cohere.client import Client

from openai import OpenAI
from langchain_openai import ChatOpenAI
from components.app_interface.configmanager import HOSTING


class LLM(ABC):
    
    def check_and_get_models_type(self) -> str:
        pass
    
    def run(self, **args):
        pass



class AnthropicClass(LLM):
    
    def __init__(self, hosting=HOSTING):
        self.config = config
        self.username = st.session_state.username
        if hosting:
            self.api_key = st.session_state.api_key
        else:
            self.api_key = config['credentials'][self.username]['provider']['api_key']
    

    def check_and_get_models_type(self):
        args = get_args(anthropic.types.model.Model)  
        models = get_args(args[1])
        model_type = st.selectbox(
        "Select the models",
        models
        )
        return model_type
    
    def run(self, model_type):
        model = ChatAnthropic(model=model_type, api_key=self.api_key)
        return model


class CohereClass(LLM):

    def __init__(self, hosting=HOSTING):
        self.config = config
        self.username = st.session_state.username
        if hosting:
            self.api_key = st.session_state.api_key
        else:
            self.api_key = config['credentials'][self.username]['provider']['api_key']
        
    def check_and_get_models_type(self):
        client = Client(
        api_key=self.api_key
        )
        models = client.models.list().models
        model_type = st.selectbox(
            "Select the models",
            [model.name for model in models if "chat" in model.endpoints]
        )
        return model_type
    
    def run(self, model_type):
        model = ChatCohere(model=model_type, cohere_api_key=self.api_key)
        return model
    
    
class OpenAIClass(LLM):
        
    def __init__(self, hosting=HOSTING):
        self.config = config
        self.username = st.session_state.username
        if hosting:
            self.api_key = st.session_state.api_key
        else:
            self.api_key = config['credentials'][self.username]['provider']['api_key']
    
    
    def check_and_get_models_type(self):
        client = Client(
        api_key=self.api_key
        )
        models = client.models.list().models
        model_type = st.selectbox(
            "Select the models",
            [model.name for model in models if "chat" in model.endpoints]
        )
        return model_type
    
    def run(self, model_type):
        model = OpenAI(model=model_type, api_key=self.api_key)
        return model


def get_model():
    mapper = {
        "Cohere": CohereClass,
        "Claude": AnthropicClass,
        "OpenAI": OpenAIClass
    }
    return mapper[st.session_state.llm_provider]
