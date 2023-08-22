import psycopg2
import streamlit as st

@st.cache_resource
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])
