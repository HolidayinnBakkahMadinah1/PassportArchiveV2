import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from io import BytesIO
import streamlit as st, pathlib, os
from utils import load_css



st.set_page_config(page_title="نظام الأرشفة", layout="wide")

def load_css(filepath):
    with open(filepath) as f:
        st.html(f"<style>{f.read()}</style>")

css_path = pathlib.Path("styles/style.css")
load_css(css_path) 


st.image("static/LargeLogo.png", width=200)

# Auth guard
if not st.session_state.get("authentication_status"):
    st.warning("يرجى تسجيل الدخول أولاً."); st.stop()
if "admin" not in st.session_state.get("user_roles", []):
    st.warning("هذه الصفحة للمسؤول فقط."); st.stop()

st.title("صفحة إدارة المسؤول")

conn = st.connection("gsheets", type=GSheetsConnection)
passports = conn.read(worksheet="Passports", usecols=list(range(12)), ttl=10).dropna(how="all")
bags      = conn.read(worksheet="Bags",      usecols=list(range(5)),  ttl=10).dropna(how="all")

st.markdown("### تحميل جميع البيانات")
if st.button("إنشاء ملف Excel"):
    buf = BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as wr:
        passports.to_excel(wr, index=False, sheet_name="Passports")
        bags.to_excel(wr, index=False, sheet_name="Bags")
    buf.seek(0)
    st.download_button("تحميل ملف Excel", buf, "HajjArchiveData.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

st.markdown("### البحث في سجلات الجوازات")
search = st.text_input("بحث برقم الجواز")
filtered = passports if not search else passports[passports["Passport Number"]
                                                  .astype(str).str.contains(search)]
st.dataframe(filtered if not filtered.empty else pd.DataFrame({"🔍": ["لا نتائج"]}))

st.markdown("### معلومات من أضاف السجلات")
if "Added By" in passports.columns:
    st.dataframe(passports[["Passport Number","Added By"]])
else:
    st.info("لا توجد معلومات عن من أضاف السجلات.")
