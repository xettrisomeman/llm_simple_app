import streamlit as st
import toml
import json
from components.app_interface.configmanager import HOSTING


CONFIG_TOML = ".streamlit/config.toml"
with open(CONFIG_TOML, 'r') as f:
    config = toml.load(f)
    

COLOR_CODE_FILE = "./color_list.json"

with open(COLOR_CODE_FILE, "r") as file:
    data = json.load(file)

PRIMARY_COLOR = config['theme']['primaryColor']
BACKGROUND_COLOR = config['theme']['backgroundColor']
SECONDARY_BACKGROUND_COLOR = config['theme']['secondaryBackgroundColor']
TEXT_COLOR = config['theme']['textColor']
FONT = config['theme']['font']


def map_to_code(color_name):
    colors_dict = {}
    for color_dict in data:
        for color, value in color_dict.items():
            colors_dict[color] = value
    return colors_dict[color_name]


def map_to_color(code):
    code_dict = {}
    for color_dict in data:
        for color, value in color_dict.items():
            code_dict[value] = color
    return code_dict[code]

st.write("Current Primary Color: ", map_to_color(PRIMARY_COLOR))
PRIMARY_COLOR = st.selectbox(
    "Select Primary Color",
     [color for color_dict in data for color, _ in color_dict.items()]
)
st.write("Current Background Color: ", map_to_color(BACKGROUND_COLOR))
BACKGROUND_COLOR = st.selectbox(
    "Select Background Color",
    [color for color_dict in data for color, _ in color_dict.items()]
)

st.write("Current Secondary Background Color: ", map_to_color(SECONDARY_BACKGROUND_COLOR))
SECONDARY_BACKGROUND_COLOR = st.selectbox(
    "Select Secondary Background Color",
    [color for color_dict in data for color, _ in color_dict.items()]
)

st.write("Current Text Color: ", map_to_color(TEXT_COLOR))
TEXT_COLOR = st.selectbox(
    "Select Text Color",
    [color for color_dict in data for color, _ in color_dict.items()]
)

st.write("Current Font Family: ", FONT)
FONT = st.selectbox(
    "Select Font Type",
    ["sans serif", "serif", "monospace"]
)


save_btn = st.button("Save", disabled=True if HOSTING else False)
if save_btn:
    config['theme']['primaryColor'] = map_to_code(PRIMARY_COLOR)
    config['theme']['backgroundColor'] = map_to_code(BACKGROUND_COLOR)
    config['theme']['secondaryBackgroundColor'] = map_to_code(SECONDARY_BACKGROUND_COLOR)
    config['theme']['textColor'] = map_to_code(TEXT_COLOR)
    config['theme']['font'] = FONT
    
    with open(CONFIG_TOML, "w") as config_file:
        toml.dump(config, config_file)
    st.rerun()