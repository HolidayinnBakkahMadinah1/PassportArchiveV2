# utils.py
import pathlib
import streamlit as st

###############################################################################
# 1) Mount /static  (call once per script, safe to call repeatedly)
###############################################################################
def mount_static():
    if st.session_state.get("_static_mounted"):
        return

    static_dir = pathlib.Path(__file__).parent / "static"
    if static_dir.exists():
        # Streamlit 1.32+ helper (otherwise use st.markdown with base64)
        st.static_file_path(str(static_dir))
        st.session_state["_static_mounted"] = True
    else:
        st.warning(f"⚠️ static folder not found: {static_dir}")


###############################################################################
# 2) Inject CSS  (lightweight; just read file and push into the page)
###############################################################################
def load_css(path: str = "styles/style.css"):
    css_path = pathlib.Path(__file__).parent / path
    if not css_path.exists():
        st.error(f"CSS file not found: {css_path}")
        return
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)
import streamlit as st

def topbar_logo(img_path: str, width: int = 120):
    """
    Insert a logo at the far left of the Streamlit-header / pages bar.
    Call once, immediately after st.set_page_config().
    """
    # Streamlit headers are rendered before the first element appears.
    # The safest trick: build a 2-column row, put the logo in the very
    # first (tiny) column and leave the second column empty.
    logo_col, _ = st.columns([1, 99])
    with logo_col:
        st.image(img_path, width=width)