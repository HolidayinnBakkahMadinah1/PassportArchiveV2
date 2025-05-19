# # utils.py
# import streamlit as st
# import pathlib

# # inject CSS ------------------------------------------------------------
# def load_css(file_path: pathlib.Path):
#     with open(file_path) as f:
#         st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# # put a logo in the Streamlit *native* navbar (works ≥ 1.40)
# def topbar_logo(path: str, width: int = 120):
#     st.logo(path, image_width=width)
# pages/ResetPassword.py ──────────────────────────────────────────────
# utils.py ────────────────────────────────────────────────────────────
import streamlit as st, pathlib, re
from supabase import create_client
from google.oauth2.service_account import Credentials
import gspread

# ---------- CSS loader ----------
def load_css(path: pathlib.Path):
    with open(path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------- logo in navbar -------
def topbar_logo(img_path: str, width: int = 120):
    st.logo(img_path, image_width=width)

# ---------- Supabase session -----
def set_session_from_supabase(auth_res, supabase_client):
    """stores email, id, role in st.session_state"""
    if not auth_res or not auth_res.session: return
    user = auth_res.user
    st.session_state["authenticated"] = True
    st.session_state["user_email"] = user.email
    st.session_state["user_id"]    = user.id

    # fetch role
    role_res = supabase_client.table("user_roles").select("role").eq("id", user.id).execute()
    role = role_res.data[0]["role"] if role_res.data else "user"
    st.session_state["role"] = role

# ---------- GSheets helpers -------
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
def get_gsheets_client():
    creds_info = st.secrets["connections"]["gsheets"]
    creds = Credentials.from_service_account_info(creds_info, scopes=SCOPES)
    gc = gspread.authorize(creds)
    sh = gc.open_by_url(creds_info["spreadsheet"])
    return gc, sh

# ---------- OCR helpers ----------
def parse_mrz(text: str) -> dict | None:
    """
    Extract MRZ fields (passport, DOB, gender, nationality) from OCR text.
    Very simplistic: look for two lines of length 44, or regex passport-like.
    """
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    lines = [l.replace(" ", "").replace("\n","") for l in lines]
    mrz = [l for l in lines if len(l) >= 40]
    if len(mrz) >= 2:
        l2 = mrz[-1]  # second MRZ line
        passport = re.sub(r"<+", "", l2[0:9])
        nat      = l2[10:13]
        dob      = l2[13:19]  # YYMMDD
        gender   = l2[20]
        # format dob to YYYY-MM-DD (assume 19xx / 20xx)
        year = int(dob[0:2])
        year += 2000 if year < 25 else 1900
        dob_fmt = f"{year}-{dob[2:4]}-{dob[4:6]}"
        return {"passport": passport, "nat": nat, "dob": dob_fmt, "gender": gender}
    return None
