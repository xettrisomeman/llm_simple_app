from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
import streamlit as st 
from utils import get_data
from prompts import (
    FACT_CHECKER_PROMPT
)
from tools import web_search

import json
from llms import get_model



model = get_model()
fact_to_check = st.text_input("Fact To Check", "Is yann lecun neurologist?")
model_type = model().check_and_get_models_type()
button = st.button("Check")
if button:
    try:
        llm = model().run(model_type=model_type)
        full_duckduckgo_input_search = (
            RunnablePassthrough.assign(
                results=lambda x: web_search(query=x["fact"], num_results=5, timelimit="y")
            )  
            | RunnableLambda(
                lambda x: {
                "fact": x["fact"],
                "context": [{"snippet": d['snippet'], 
                                "url": d['link']}  for d in x['results']]
                }
                ) 
        )

        full_search_chain = full_duckduckgo_input_search | RunnablePassthrough.assign(
            fact=RunnablePassthrough.assign(
                context=lambda x: [get_data(data['url']) for data in x['context']]
        ) 
        ) | RunnableLambda(
                lambda x: x['fact']
            ) | FACT_CHECKER_PROMPT | llm | StrOutputParser()
        
        check_fact = full_search_chain.invoke({
            "fact": fact_to_check
        })
        st.write(check_fact)
    except Exception as e:
        st.error(e)