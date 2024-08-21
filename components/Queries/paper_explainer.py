from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
from pdfminer.high_level import extract_text
from prompts import PAPER_EXPLAINER_PROMPT
from llms import get_model


model = get_model()
uploaded_file = st.file_uploader(
    "Choose a file", accept_multiple_files=False,
    type='pdf'
    )
if uploaded_file:
    model_type = model().check_and_get_models_type()
    button = st.button("Explain Paper")
    if button:
        try:
            llm = model().run(model_type=model_type)
            paper_explainer = RunnablePassthrough.assign(
                paper=lambda x: x['paper']
                ) | PAPER_EXPLAINER_PROMPT | llm | StrOutputParser()
        
            text_from_pdf = extract_text(uploaded_file)
            explain = paper_explainer.invoke({
                "paper": text_from_pdf
                })
            st.write(explain)
        except Exception as e:
            st.error(e)