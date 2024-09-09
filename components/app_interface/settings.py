from components.app_interface.configmanager import YAML_FILE
import streamlit as st
import yaml

llms = [
    "Cohere",
    "OpenAI",
    "Claude"
]

def settings(username: str | None, config, hosting):
    if not hosting:
        current_user = st.session_state.username
        api_key = config['credentials'][current_user]['provider'].get("api_key", None)
        llm_provider_ = config['credentials'][current_user]['provider'].get("llm_provider", None)
        if api_key:
            llm_provider = st.selectbox(
                "Select llm provider",
                ("Cohere", "OpenAI", "Claude"), index=llms.index(llm_provider_), disabled=True)
            llm_key = st.text_input("Api key: ", api_key, disabled=True)
            button = st.button("Delete")
            if button:
                config['credentials'][username]['provider'] = {"llm": None, "api_key": None}
                with open(YAML_FILE, "w") as file:
                    yaml.dump(config, file, default_flow_style=True)
                    st.rerun()
        else:
            llm_provider = st.selectbox(
                "Select llm provider:",
                ("Cohere", "OpenAI", "Claude"),
            )
            llm_key = st.text_input("Api key: ")
            button = st.button("save")
            if button:
                if not llm_key:
                    st.warning("Api Key is required!")
                else:
                    config['credentials'][username]['provider']['llm'] = llm_provider
                    config[ 'credentials'][username]['provider']['api_key'] = llm_key
                    with open(YAML_FILE, "w") as file:
                        yaml.dump(config, file, default_flow_style=False)
                    st.rerun()
    else:
        current_user = st.session_state.username
        api_key = st.session_state.api_key
        llm_provider_ = st.session_state.llm_provider
        if api_key:
            llm_provider = st.selectbox(
                "Select llm provider",
                ("Cohere", "OpenAI", "Claude"), index=llms.index(llm_provider_), disabled=True)
            llm_key = st.text_input("Api key: ", api_key, disabled=True)
            button = st.button("Delete")
            if button:
                st.session_state.api_key = None
                st.session_state.llm_provider = None
                st.rerun()
        else:
            llm_provider = st.selectbox(
                "Select llm provider:",
                ("Cohere", "OpenAI", "Claude"),
            )
            llm_key = st.text_input("Api key: ")
            button = st.button("save")
            if button:
                if not llm_key:
                    st.warning("Api Key is required!")
                else:
                    st.session_state.api_key = llm_key
                    st.session_state.llm_provider = llm_provider
                    st.rerun()