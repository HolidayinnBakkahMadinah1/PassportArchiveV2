# utils.py
import streamlit as st
import pathlib

# inject CSS ------------------------------------------------------------
def load_css(file_path: pathlib.Path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# put a logo in the Streamlit *native* navbar (works ≥ 1.40)
def topbar_logo(path: str, width: int = 120):
    st.logo(path, image_width=width)
