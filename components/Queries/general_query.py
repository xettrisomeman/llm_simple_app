from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
from prompts import (
    GENERAL_QUERY_PROMPT,
    PROMPT_DUCKDUCKGO_SEARCH
)
from llms import get_model
import json

from utils import get_data
from tools import web_search


model = get_model()
question = st.text_input("Question: ", "Give information about latest man city transfers.")
button = st.button("Search", type="primary")
try:
    model_type = model().check_and_get_models_type()
    if button:
        llm = model().run(model_type=model_type)
        duckduckgo_input_search = RunnablePassthrough.assign(
            output = RunnableLambda(lambda x: {"input": x['input']}) | PROMPT_DUCKDUCKGO_SEARCH | llm | StrOutputParser() | json.loads 
        )
        full_duckduckgo_input_search = duckduckgo_input_search | (
            RunnablePassthrough.assign(
                results=lambda x: web_search(query=x["output"][0], num_results=5, timelimit=x['output'][1])
            )  
            | RunnableLambda(
                lambda x: {
                "question": x["input"],
                "content": [{"snippet": d['snippet'], 
                                "url": d['link']}  for d in x['results']]
                }
                ) 
        )

        full_search_chain = full_duckduckgo_input_search | RunnablePassthrough.assign(
            text=RunnablePassthrough.assign(
                content=lambda x: [get_data(data['url']) for data in x['content']]
        ) 
        ) | RunnableLambda(
                lambda x: x['text']
            ) | GENERAL_QUERY_PROMPT | llm | StrOutputParser()
        
        query = full_search_chain.invoke({
            "input": question
        })
        st.write(query)
        
    else:
        query = None
except Exception as e:
    st.error(e)
    