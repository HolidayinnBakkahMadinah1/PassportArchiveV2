# import streamlit as st, pandas as pd, pathlib
# from datetime import date
# from google.oauth2.service_account import Credentials
# import gspread
# from utils import load_css

# st.set_page_config(page_title="الحقائب", layout="wide")
# load_css(pathlib.Path("styles/style.css"))

# # Auth guard
# if not st.session_state.get("authentication_status"):
#     st.info("يرجى تسجيل الدخول لاستخدام النظام.")
#     st.stop()

# # ── GSpread client ────────────────────────────────────────────────────
# SCOPES = [
#     "https://www.googleapis.com/auth/spreadsheets",
#     "https://www.googleapis.com/auth/drive",
# ]
# creds = Credentials.from_service_account_info(
#     st.secrets["connections"]["gsheets"], scopes=SCOPES
# )
# gc = gspread.authorize(creds)
# sh = gc.open_by_url(st.secrets["connections"]["gsheets"]["spreadsheet"])
# ws_bags = sh.worksheet("Bags")

# existing_B = pd.DataFrame(ws_bags.get_all_records())

# arrival_gates = ["المطار","القطار","كيلو ٩"]
# nationalities = ["باكستان","أندونيسيا","أخرى"]

# st.title("تسجيل بيانات الحقائب")
# with st.form("BagsForm"):
#     bag_number    = st.text_input("رقم الحقيبة*")
#     num_passports = st.number_input("عدد الجوازات داخل الحقيبة*", min_value=1, step=1)
#     arrival_gate  = st.selectbox("بوابة الوصول*", arrival_gates)
#     arrival_date  = st.date_input("تاريخ الوصول*", value=date.today())
#     nationality   = st.selectbox("الجنسية*", nationalities)
#     if nationality == "أخرى":
#         nationality = st.text_input("الرجاء تحديد الجنسية")
#     if st.form_submit_button("تسجيل"):
#         if not bag_number:
#             st.warning("رقم الحقيبة حقل إجباري.")
#             st.stop()
#         new_row = [
#             bag_number, num_passports, arrival_gate,
#             arrival_date.strftime("%Y-%m-%d"), nationality,
#         ]
#         ws_bags.append_row(new_row, value_input_option="USER_ENTERED")
#         st.success("تم حفظ بيانات الحقيبة بنجاح!")
# pages/Bags.py ───────────────────────────────────────────────────────
#---------------------v2.2---------------------
# import streamlit as st, pandas as pd, pathlib
# from datetime import date, datetime
# from utils import load_css, get_gsheets_client

# st.set_page_config(page_title="الحقائب", layout="wide")
# load_css(pathlib.Path("styles/style.css"))

# if not st.session_state.get("authenticated"):
#     st.info("يرجى تسجيل الدخول لاستخدام النظام.")
#     st.stop()

# user_email = st.session_state["user_email"]

# gc, sh = get_gsheets_client()
# ws_bags = sh.worksheet("Bags")

# st.title("تسجيل بيانات الحقائب")

# with st.form("bag_form"):
#     bag_no   = st.text_input("رقم الحقيبة*")
#     count    = st.number_input("عدد الجوازات داخل الحقيبة*", min_value=1, step=1)
#     gate     = st.selectbox("بوابة الوصول*", ["المطار","القطار","كيلو ٩"])
#     arr_date = st.date_input("تاريخ الوصول*", value=date.today())
#     nat      = st.text_input("الجنسية*")
#     sub      = st.form_submit_button("حفظ السجل")

# if sub:
#     if not bag_no:
#         st.warning("رقم الحقيبة حقل إجباري.")
#         st.stop()
#     row = [
#         datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         bag_no, count, gate, arr_date.strftime("%Y-%m-%d"), nat,
#         user_email,
#     ]
#     ws_bags.append_row(row, value_input_option="USER_ENTERED")
#     st.success("تم حفظ السجل.")
#----------------------v2.3----------------------------
# pages/Bags.py
import streamlit as st
import pandas as pd
import pathlib
from datetime import date
from google.oauth2.service_account import Credentials  # no change
import gspread
from utils import load_css

st.set_page_config(page_title="الحقائب", layout="wide")
load_css(pathlib.Path("styles/style.css"))

# Auth guard
if not st.session_state.get("authenticated"):
    st.info("يرجى تسجيل الدخول لاستخدام النظام.")
    st.stop()

# ── GSpread client ────────────────────────────────────────────────────
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
# ⬅️ UPDATED: same as above, point to connections.gsheets
creds = Credentials.from_service_account_info(
    st.secrets["connections"]["gsheets"],
    scopes=SCOPES
)
gc = gspread.authorize(creds)
sh = gc.open_by_url(
    st.secrets["connections"]["gsheets"]["spreadsheet"]
)
ws_bags = sh.worksheet("Bags")

existing_B = pd.DataFrame(ws_bags.get_all_records())

arrival_gates = ["المطار","القطار","كيلو ٩"]
nationalities = ["باكستان","أندونيسيا","أخرى"]

st.title("تسجيل بيانات الحقائب")
with st.form("BagsForm"):
    bag_number    = st.text_input("رقم الحقيبة*")
    num_passports = st.number_input("عدد الجوازات داخل الحقيبة*", min_value=1, step=1)
    arrival_gate  = st.selectbox("بوابة الوصول*", arrival_gates)
    arrival_date  = st.date_input("تاريخ الوصول*", value=date.today())
    nationality   = st.selectbox("الجنسية*", nationalities)
    if nationality == "أخرى":
        nationality = st.text_input("الرجاء تحديد الجنسية")
    if st.form_submit_button("تسجيل"):
        if not bag_number:
            st.warning("رقم الحقيبة حقل إجباري.")
            st.stop()
        new_row = [
            bag_number,
            num_passports,
            arrival_gate,
            arrival_date.strftime("%Y-%m-%d"),
            nationality,
        ]
        ws_bags.append_row(new_row, value_input_option="USER_ENTERED")
        st.success("تم حفظ بيانات الحقيبة بنجاح!")
