import json
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
from prompts import DATA_EXTRACTOR_PROMPT
from llms import get_model

EXAMPLE_TEXT = """
Nepal, officially the Federal Democratic Republic of Nepal, is a landlocked country in South Asia. 
It is mainly situated in the Himalayas, but also includes parts of the Indo-Gangetic Plain. 
It borders the Tibet Autonomous Region of China to the north, 
and India to the south, east, and west, while it is narrowly separated from 
Bangladesh by the Siliguri Corridor, and from Bhutan by the Indian state of Sikkim. 
Nepal has a diverse geography, including fertile plains, subalpine forested hills, 
and eight of the world's ten tallest mountains, including Mount Everest, 
the highest point on Earth. Kathmandu is the nation's capital and the largest city. 
Nepal is a multi-ethnic, multi-lingual, multi-religious and multi-cultural state,
with Nepali as the official language.

The name "Nepal" is first recorded in texts from the Vedic period of the Indian subcontinent, 
the era in ancient Nepal when Hinduism was founded, the predominant religion of the country. 
In the middle of the first millennium BC, Gautama Buddha, the founder of Buddhism, was born in Lumbini
in southern Nepal. Parts of northern Nepal were intertwined with the culture of Tibet. 
The centrally located Kathmandu Valley is intertwined with the culture of Indo-Aryans, 
and was the seat of the prosperous Newar confederacy known as Nepal Mandala. 
The Himalayan branch of the ancient Silk Road was dominated by the valley's traders. 
The cosmopolitan region developed distinct traditional art and architecture. 
By the 18th century, the Gorkha Kingdom achieved the unification of Nepal. 
The Shah dynasty established the Kingdom of Nepal and later formed an alliance with the British Empire,
under its Rana dynasty of premiers. The country was never colonised but served as a 
buffer state between Imperial China and British India. Parliamentary democracy was introduced in 
1951 but was twice suspended by Nepalese monarchs, in 1960 and 2005. 
The Nepalese Civil War in the 1990s and early 2000s resulted in the establishment of a 
secular republic in 2008, ending the world's last Hindu monarchy.

The Constitution of Nepal, adopted in 2015, affirms the country as a secular federal 
parliamentary republic divided into seven provinces. 
Nepal was admitted to the United Nations in 1955, and friendship treaties 
were signed with India in 1950 and China in 1960. 
Nepal hosts the permanent secretariat of the South Asian Association for Regional Cooperation (SAARC),
of which it is a founding member. Nepal is also a member of the Non-Aligned Movement and 
the Bay of Bengal Initiative. """

EXAMPLE_INSTRUCTIONS = """
create a multiple choice questions
"""

model = get_model()
text = st.text_area("Enter text: ",EXAMPLE_TEXT, height=500)
instruction = st.text_input("Enter instructions: ", EXAMPLE_INSTRUCTIONS)
model_type = model().check_and_get_models_type()
button = st.button("Extract")
if button:
    if not text:
        st.warning("Text field should not be empty.")
    elif not instruction:
        st.warning("Instruction field should not be empty.")
    else:
        try:
            llm = model().run(model_type=model_type)
            extract_data = RunnablePassthrough.assign(
                text = lambda x: x['text'],
                instruction = lambda x: x['instruction']) | DATA_EXTRACTOR_PROMPT | llm | StrOutputParser() | json.loads
            output = extract_data.invoke(
                {
                    "text": text,
                    "instruction": instruction
                }
            )
            st.write(output)
            file_type, data = output[0], output[1]
            if file_type == "text":
                st.write(data)
            st.download_button(
                label = f"Download {file_type}",
                data=data,
                file_name= f"{hash(instruction)}.{file_type}",
                mime=f"text/{file_type}"
            )
        except Exception as e:
            st.error(e)