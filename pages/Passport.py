import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import date
import streamlit as st, pathlib, os
from utils import mount_static, load_css
from utils import topbar_logo


st.set_page_config(page_title="نظام الأرشفة", layout="wide")

def load_css(filepath):
    with open(filepath) as f:
        st.html(f"<style>{f.read()}</style>")

css_path = pathlib.Path("styles/style.css")
load_css(css_path)
st.image("static/LargeLogo.png", width=200)

# ── Auth guard ──
if not st.session_state.get("authentication_status"):
    st.warning("يرجى تسجيل الدخول أولاً.")
    st.stop()
roles = st.session_state.get("user_roles", [])
if not any(r in roles for r in ("admin", "editor","user")):
    st.error("ليس لديك صلاحية الوصول إلى هذه الصفحة.")
    st.stop()

# ── UI & logic (unchanged) ──
st.title("أرشفة الجوازات")
st.markdown("أدخل معلومات الجواز في الأسفل:")

conn = st.connection("gsheets", type=GSheetsConnection)
existing_dataP = conn.read(worksheet="Passports", usecols=list(range(12)), ttl=10)
existing_dataB = conn.read(worksheet="Bags",      usecols=list(range(5)),  ttl=10)
existing_dataP = existing_dataP.dropna(how='all')
existing_dataB = existing_dataB.dropna(how='all')

bags_list     = existing_dataB.iloc[:, 0].tolist()
arrival_gates = ["المطار", "القطار", "كيلو ٩"]
notes_options = ["لا يوجد","متوفى","مفقود","تم إلقاء القبض","تم ترحيلة"]

with st.form("PassportForm"):
    Passport_num = st.text_input("رقم جواز السفر*")
    Barcode      = st.text_input("باركود نسك*")
    NameEN       = st.text_input("الإسم باللغة الانجليزية*")
    NameAR       = st.text_input("الإسم باللغة العربية*")
    DateOfBirth  = st.date_input("تاريخ الميلاد*", value=date(1990,1,1),
                                 min_value=date(1900,1,1), max_value=date.today())
    Gender       = st.selectbox("الجنس*", ("Male","Female"))
    Nationality  = st.selectbox("الجنسية*", ("باكستان","أندونيسيا","أخرى"))
    if Nationality == "أخرى":
        Nationality = st.text_input("الرجاء تحديد الجنسية")
    Bag          = st.selectbox("رقم الحقيبة*", options=bags_list)
    Arrival_gate = st.selectbox("بوابة الوصول*", options=arrival_gates)
    Arrival_date = st.date_input("تاريخ الوصول*", value=date.today())
    Departure_date = st.date_input("تاريخ المغادرة", value=date.today())
    Notes        = st.selectbox("الملاحظات", notes_options)

    if st.form_submit_button("تسجيل"):
        if not Passport_num:
            st.warning("الرجاء إدخال رقم الجواز."); st.stop()
        new_row = pd.DataFrame([{
            "Passport Number": Passport_num,
            "Barcode": Barcode,
            "Name in English": NameEN,
            "Name in Arabic": NameAR,
            "Date of Birth": DateOfBirth,
            "Gender": Gender,
            "Nationality": Nationality,
            "Bag Number": Bag,
            "Arrival Gate": Arrival_gate,
            "Arrival Date": Arrival_date,
            "Departure Date": Departure_date,
            "Notes": Notes,
        }])
        # new – worksheet + dataframe as keywords:
        conn.update(
            worksheet="Bags",
            dataframe=pd.concat([existing_dataP, new_row], ignore_index=True),
        )

        st.success("تم حفظ بيانات الجواز بنجاح!")
