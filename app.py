from functools import partial
import streamlit as st
from components.app_interface.configmanager import config, YAML_FILE, HOSTING
from components.app_interface.navigation import AccountView
from components.app_interface.settings import settings
import yaml



account_view = AccountView(config)

if not HOSTING:
    CURRENT_USER = config['credentials'].get('current_user', None)
    st.session_state.username = CURRENT_USER
    USER_LOGGED_IN = True if CURRENT_USER else False
    api_key = config['credentials'][CURRENT_USER]['provider'].get("api_key", None)
    llm_provider = config['credentials'][CURRENT_USER]['provider']['llm']

else:
    try:
        CURRENT_USER = st.session_state.username
    except:
        st.session_state.username = None
        CURRENT_USER = st.session_state.username
    try:
        api_key = st.session_state.api_key
        llm_provider = st.session_state.llm_provider
    except:
        st.session_state.api_key = None
        api_key = st.session_state.api_key
        
        st.session_state.llm_provider = None
        llm_provider = st.session_state.llm_provider
    
    USER_LOGGED_IN = True if CURRENT_USER else False
    

def login_register_view():
    if not USER_LOGGED_IN:
        if not HOSTING:
            tab1, tab2, tab3 = st.tabs(["Login", "Register", "Account Details"])
            with tab1:
                try:
                    username = account_view.login()
                    if username:
                        st.rerun()
                except Exception as e:
                    st.warning(e)
            with tab2:
                try:
                    account_view.register()
                except Exception as e:
                    st.warning(e)
            with tab3:
                account_view.show_details()
        else:
            tab1, tab2 = st.tabs(["Login", "Account Details"])
            with tab1:
                try:
                    username = account_view.login()
                    if username:
                        st.rerun()
                except Exception as e:
                    st.warning(e)
            with tab2:
                account_view.show_details()
            

def logout_view():
    button = st.button("Logout")
    if button:
        if HOSTING:
            st.session_state.username = None
            st.rerun()
        config['credentials']['current_user'] = None
        with open(YAML_FILE, "w") as file:
            yaml.dump(config, file, default_flow_style=False)
        st.rerun()



page_dict = {}
if USER_LOGGED_IN:
    ## ACCOUNT
    settings = partial(settings, CURRENT_USER, config, HOSTING)
    settings_page = st.Page(
        settings,
        title="Settings",
        icon=":material/settings:"
    )
    logout_page = st.Page(
            logout_view,
                      title="Logout", 
                      icon=":material/logout:")
    change_theme_page = st.Page(
        "components/app_interface/change_theme.py",
        title = "Change Theme",
        icon = ":material/palette:"
    )
    app_pages = [logout_page, settings_page, change_theme_page]
    
    ##########
    
    ## QUERY
    
    if api_key:
        general_query_page = st.Page(
            "components/Queries/general_query.py",
            title="General Query",
            icon=":material/search:",
            default=True
        )
    
        text_summarizer_page = st.Page(
            "components/Queries/summarizer.py",
            title="Summarizer",
            icon=":material/summarize:"
        )
        
        paper_explainer_page = st.Page(
            "components/Queries/paper_explainer.py",
            title="Explain Paper",
            icon=":material/article:"
        )
        
        fact_checker_page = st.Page(
            "components/Queries/fact_checker.py",
            title="Fact Checker",
            icon=":material/fact_check:"
        )
        
        data_extractor_page = st.Page(
            "components/Queries/data_extractor.py",
            title="Data Extractor",
            icon=":material/analytics:"
        )
        page_dict['Queries'] = [general_query_page, 
                                text_summarizer_page, 
                                paper_explainer_page, 
                                fact_checker_page,
                                data_extractor_page]
            
    
    pg = st.navigation({"App": app_pages} | page_dict)
else:
    pg = st.navigation([st.Page(login_register_view)])


pg.run()