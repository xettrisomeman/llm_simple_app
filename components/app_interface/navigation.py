import streamlit as st 
from typing import Any, Dict
from components.app_interface.configmanager import YAML_FILE
import yaml


if __name__ == "__main__":
    from account import (
        Login,
        Register,
    )
    from components.app_interface.exceptions import (
        IncorrectPassword,
        UsernameDoesNotExist,
        UsernameAlreadyExist,
        PasswordDoesNotMatch
     )
else:
    from components.app_interface.account import (
        Login,
        Register
    )
    from components.app_interface.exceptions import (
        IncorrectPassword,
        UsernameDoesNotExist,
        UsernameAlreadyExist,
        PasswordDoesNotMatch
    )

@st.fragment
class AccountView:

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.username: str


    def login(self):
        username = st.text_input("Username: ", key="login")
        password = st.text_input("Enter password: ", type="password")
            
        submit_enabled = username and password
        button = st.button("Login", type="primary", disabled = not submit_enabled)
        if button:
            login = Login(
            username = username,
            password = password
                        )
            if login.username in self.config['credentials']:
                if login.password == self.config['credentials'][login.username]['password']:
                    self.username = login.username
                    st.session_state.username = self.username
                    self.config['credentials']['current_user'] = login.username
                    with open(YAML_FILE, "w") as file:
                        yaml.dump(self.config, file, default_flow_style=False)
                    return login.username
                else:
                    raise IncorrectPassword
            else:
                raise UsernameDoesNotExist

    def register(self):
        username = st.text_input("Username: ", key="register")
        password = st.text_input("Password: ", type="password")
        password2 = st.text_input("Re-type Password : ", type="password")

        submit_enabled = username and password and password2
        button = st.button("Register", type="primary", disabled=not submit_enabled)
        if button:
            register = Register(
            username = username,
            password = password,
            password2 = password2
                                )
            if register.username not in self.config['credentials']:
                if register.password == register.password2:
                    self.config['credentials'][register.username] = {}
                    self.config['credentials'][register.username]['password'] = register.password
                    
                    self.config['credentials'][register.username]['provider'] = {}
                    self.config['credentials'][register.username]['provider']['llm'] = None
                    self.config['credentials'][register.username]['provider']['api_key'] = None
                    with open(YAML_FILE, "w") as file:
                        yaml.dump(self.config, file, default_flow_style=False)
                else:
                    raise PasswordDoesNotMatch
            else:
                raise UsernameAlreadyExist 


    def show_details(self):
        return st.write(self.config['credentials'])

