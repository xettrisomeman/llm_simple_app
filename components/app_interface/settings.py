from components.app_interface.configmanager import YAML_FILE
import streamlit as st
import yaml


def settings(username: str | None, config):
    api_key = config['credentials'][username]['provider'].get("api_key")
    if api_key:
        llm_provider = st.selectbox(
            "Select llm provider",
            ("Cohere", "OpenAI", "Claude"), disabled=True)
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
