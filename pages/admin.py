# import streamlit as st
# from streamlit_gsheets import GSheetsConnection
# import pandas as pd
# from io import BytesIO
# import streamlit as st, pathlib, os
# from utils import load_css



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
# if "admin" not in st.session_state.get("user_roles", []):
#     st.warning("هذه الصفحة للمسؤول فقط."); st.stop()

# st.title("صفحة إدارة المسؤول")

# conn = st.connection("gsheets", type=GSheetsConnection)
# passports = conn.read(worksheet="Passports", usecols=list(range(12)), ttl=10).dropna(how="all")
# bags      = conn.read(worksheet="Bags",      usecols=list(range(5)),  ttl=10).dropna(how="all")

# st.markdown("### تحميل جميع البيانات")
# if st.button("إنشاء ملف Excel"):
#     buf = BytesIO()
#     with pd.ExcelWriter(buf, engine="openpyxl") as wr:
#         passports.to_excel(wr, index=False, sheet_name="Passports")
#         bags.to_excel(wr, index=False, sheet_name="Bags")
#     buf.seek(0)
#     st.download_button("تحميل ملف Excel", buf, "HajjArchiveData.xlsx",
#                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# st.markdown("### البحث في سجلات الجوازات")
# search = st.text_input("بحث برقم الجواز")
# filtered = passports if not search else passports[passports["Passport Number"]
#                                                   .astype(str).str.contains(search)]
# st.dataframe(filtered if not filtered.empty else pd.DataFrame({"🔍": ["لا نتائج"]}))

# st.markdown("### معلومات من أضاف السجلات")
# if "Added By" in passports.columns:
#     st.dataframe(passports[["Passport Number","Added By"]])
# else:
#     st.info("لا توجد معلومات عن من أضاف السجلات.")
# pages/admin.py ──────────────────────────────────────────────────────
import streamlit as st, pandas as pd, pathlib
from io import BytesIO
from utils import load_css, get_gsheets_client

st.set_page_config(page_title="إدارة المسؤول", layout="wide")
load_css(pathlib.Path("styles/style.css"))
st.image("static/LargeLogo.png", width=160)

if "admin" not in st.session_state.get("role",""):
    st.error("هذه الصفحة للمسؤول فقط."); st.stop()

gc, sh = get_gsheets_client()
ws_passports = sh.worksheet("Passports")
ws_bags      = sh.worksheet("Bags")

df_p = pd.DataFrame(ws_passports.get_all_records())
df_b = pd.DataFrame(ws_bags.get_all_records())

st.header("تنزيل جميع البيانات Excel")
if st.button("إنشاء ملف Excel"):
    buf = BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as wr:
        df_p.to_excel(wr, index=False, sheet_name="Passports")
        df_b.to_excel(wr, index=False, sheet_name="Bags")
    buf.seek(0)
    st.download_button("تحميل", buf, "ArchiveData.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

st.header(" البحث في سجلات الجوازات")
q = st.text_input("بحث (رقم الجواز)")
filtered = df_p if not q else df_p[df_p["Passport Number"].astype(str).str.contains(q)]
st.dataframe(filtered)

st.header("معلومات المُدخل")
if "SubmittedBy" in df_p.columns:
    st.dataframe(df_p[["Passport Number","SubmittedBy"]])
else:
    st.info("لا توجد معلومات عن المُدخل.")
