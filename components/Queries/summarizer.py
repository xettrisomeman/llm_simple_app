from langchain_core.runnables import  RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
from prompts import (

    SUMMARIZER_PROMPT
)
from llms import get_model



EXAMPLE_TEXT = """Accelerationism is a range of revolutionary and reactionary ideas in left-wing and right-wing 
ideologies that call for the drastic intensification of capitalist growth, technological change, 
infrastructure sabotage and other processes of social change to destabilize existing systems and 
create radical social transformations, otherwise referred to as "acceleration".
It has been regarded as an ideological spectrum divided into mutually contradictory left-wing and 
right-wing variants, both of which support the indefinite intensification of capitalism and its 
structures as well as the conditions for a technological singularity, a hypothetical 
point in time at which technological growth becomes uncontrollable and irreversible.

Various ideas, including Gilles Deleuze and Félix Guattari's idea of deterritorialization, 
Jean Baudrillard's proposals for "fatal strategies", and aspects of the theoretical systems 
and processes developed by English philosopher and later Dark Enlightenment 
commentator Nick Land, are crucial influences on accelerationism, which aims to 
analyze and subsequently promote the social, economic, cultural, and libidinal forces 
that constitute the process of acceleration.[8] While originally used by the far-left, the term 
has, in a manner strongly distinguished from original accelerationist theorists, 
been used by right-wing extremists such as neo-fascists, neo-Nazis, white nationalists 
and white supremacists to increasingly refer to an "acceleration" of racial conflict through 
assassinations, murders and terrorist attacks as a means to violently achieve a white ethnostate.

While predominantly a political strategy suited to the industrial economy, acceleration has 
recently been discussed in debates about humanism and artificial intelligence. 
Yuk Hui and Louis Morelle consider acceleration and the "Singularity Hypothesis".
James Brusseau discusses acceleration as an ethics of innovation where humanistic dilemmas 
caused by AI innovation are resolved by still more innovation, as opposed to limiting or 
slowing the technology. A movement known as effective accelerationism (abbreviated to e/acc) 
advocates for technological progress "at all costs"
"""


model = get_model()
query = st.text_area("Text ", EXAMPLE_TEXT, height=400)
button = st.button("Summarize", type="primary")
try:
    model_type = model().check_and_get_models_type()
    if button:
        llm = model().run(model_type=model_type)
        summarizer_chain = RunnablePassthrough.assign(
            text=lambda x: x['text']
        ) | SUMMARIZER_PROMPT | llm | StrOutputParser()
        summarized = summarizer_chain.invoke({
            "text": query
        })
        
        st.write(summarized)
    else:
        summarizer_chain = None
except Exception as e:
    st.error(e)