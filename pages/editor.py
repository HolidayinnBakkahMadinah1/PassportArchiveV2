# pages/editor.py ─────────────────────────────────────────────────────
import streamlit as st, pandas as pd, pathlib
from utils import load_css, get_gsheets_client

st.set_page_config(page_title="تعديل السجلات", layout="wide")
load_css(pathlib.Path("styles/style.css"))

role = st.session_state.get("role","user")
if role not in ("admin","editor"):
    st.error("ليست لديك صلاحية لدخول هذه الصفحة."); st.stop()

gc, sh = get_gsheets_client()
ws = sh.worksheet("Passports")

df = pd.DataFrame(ws.get_all_records())
st.title("تعديل سجلات الجوازات")

query = st.text_input("ابحث بالرقم أو الاسم:")
if query:
    mask = df["Passport Number"].astype(str).str.contains(query) | \
           df.get("NameEN","").str.contains(query, case=False, na=False)
    df_view = df[mask]
else:
    df_view = df.copy()

st.dataframe(df_view)

if not df_view.empty:
    sel = st.selectbox("اختر رقم الجواز للتعديل", df_view["Passport Number"].astype(str))
    rec = df[df["Passport Number"].astype(str)==sel].iloc[0]

    with st.form("edit_form"):
        bag  = st.text_input("رقم الحقيبة", rec["Bag Number"])
        dob  = st.text_input("تاريخ الميلاد", rec["Date of Birth"])
        gen  = st.selectbox("الجنس", ["M","F"], index=(0 if rec["Gender"]=="M" else 1))
        nat  = st.text_input("الجنسية", rec["Nationality"])
        note = st.text_input("ملاحظات", rec.get("Notes",""))
        save = st.form_submit_button("حفظ التعديل")

    if save:
        # find row index (1-based, inc. header)
        row_idx = df.index[df["Passport Number"].astype(str)==sel][0] + 2
        ws.update(f"B{row_idx}:H{row_idx}",
                  [[bag, dob, gen, nat, rec["Barcode"], note]])
        st.success("تم الحفظ! أعد التحميل لرؤية التحديث.")
