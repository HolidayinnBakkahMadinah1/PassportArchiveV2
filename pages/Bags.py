# import streamlit as st
# from streamlit_gsheets import GSheetsConnection
# import pandas as pd
# from datetime import date
# import streamlit as st, pathlib, os
# from utils import mount_static, load_css
# from utils import topbar_logo


# st.set_page_config(page_title="نظام الأرشفة", layout="wide")

# def load_css(filepath):
#     with open(filepath) as f:
#         st.html(f"<style>{f.read()}</style>")

# css_path = pathlib.Path("styles/style.css")
# load_css(css_path)

# st.image("static/LargeLogo.png", width=200)

# # Auth guard
# if not st.session_state.get("authentication_status"):
#     st.warning("يرجى تسجيل الدخول أولاً."); st.stop()
# if not any(r in st.session_state.get("user_roles", []) for r in ("admin","editor","user")):
#     st.error("ليس لديك صلاحية الوصول."); st.stop()

# # UI
# st.title("تسجيل بيانات الحقائب")
# conn = st.connection("gsheets", type=GSheetsConnection)
# existing = conn.read(worksheet="Bags", usecols=list(range(5)), ttl=10)
# existing = existing.dropna(how="all")
# arrival_gates = ["المطار","القطار","كيلو ٩"]
# nationalities = ["باكستان","أندونيسيا","أخرى"]

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
#             st.warning("رقم الحقيبة حقل إجباري."); st.stop()
#         new_row = pd.DataFrame([{
#             "Bag Number": bag_number,
#             "Number of Passports": num_passports,
#             "Arrival Gate": arrival_gate,
#             "Arrival Date": arrival_date,
#             "Nationality": nationality,
#         }])
#         full_df = pd.concat([existing, new_row], ignore_index=True)
#         # ← again, use .write()
#         conn.write(full_df, worksheet="Bags")
#         st.success("تم حفظ بيانات الحقيبة بنجاح!")
import streamlit as st, pandas as pd, pathlib
from datetime import date
from google.oauth2.service_account import Credentials
import gspread
from utils import load_css

st.set_page_config(page_title="الحقائب", layout="wide")
load_css(pathlib.Path("../styles/style.css"))

# Auth guard
if not st.session_state.get("authentication_status"):
    st.info("يرجى تسجيل الدخول لاستخدام النظام.")
    st.stop()

# ── GSpread client ────────────────────────────────────────────────────
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
creds = Credentials.from_service_account_info(
    st.secrets["connections"]["gsheets"], scopes=SCOPES
)
gc = gspread.authorize(creds)
sh = gc.open_by_url(st.secrets["connections"]["gsheets"]["spreadsheet"])
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
            bag_number, num_passports, arrival_gate,
            arrival_date.strftime("%Y-%m-%d"), nationality,
        ]
        ws_bags.append_row(new_row, value_input_option="USER_ENTERED")
        st.success("تم حفظ بيانات الحقيبة بنجاح!")
