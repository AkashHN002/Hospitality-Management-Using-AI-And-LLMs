import streamlit as st
import os

from Templates.Streamlit_layout import DataTransformation
from src.config import Budget_configuration as budget_config
from src.config import Timeline_configuration as timeline_config
from src.config import assumption_config
from src.Components.load_data_model import save_data_model
from src.logger import logging

st.set_page_config(layout="wide", page_title="Data Transformation Tool")


st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTitle {
        color: #2c3e50;
        padding-bottom: 2rem;
    }
    .stSelectbox > label {
        font-size: 1.2rem;
        color: #34495e;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🔄 Data Transformation Tool")
st.markdown("""
    <div style='background-color: #B0E0E6  ; padding: 1rem; border-radius: 5px; margin-bottom: 2rem;'>
    Transform the data efficiently. Select the sheet to transformation below.
    </div>
""", unsafe_allow_html=True)

sheet_config = [
    budget_config.ConfigManager(),
    timeline_config.ConfigManager(),
    assumption_config.ConfigManager()
]

def main(idx):   
        
    config = sheet_config[idx]
    data_transformation_config = config.get_data_config()
    obj = DataTransformation(data_transformation_config)
    obj.perform_all_task()


options = {0: "Select an option", 1: "Budget", 2: "Timeline", 3: "Assumption"}

col1,_,_= st.columns(3)
with col1:

    st.markdown(
        "<h4 style='font-size: 28px; margin-bottom: 5px;'>Select a Sheet Name</h4>",
        unsafe_allow_html=True
    )

    ind = st.selectbox(
        "Select the file to be processed:",
        options=list(options.keys()),
        format_func=lambda x: options[x],
        index=None,
        label_visibility='collapsed' 
    )


if __name__ == '__main__':
    if ind is not None:
        if ind != 0:
            try:
                main(ind - 1)
            except Exception as e:
                logging.error(f"Error occured in {options[ind]} - {e}")
                raise e 
