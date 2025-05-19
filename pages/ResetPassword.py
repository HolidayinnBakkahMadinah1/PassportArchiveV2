# pages/ResetPassword.py ──────────────────────────────────────────────
import streamlit as st
from supabase import create_client
from utils import load_css
import pathlib

st.set_page_config(page_title="إعادة تعيين كلمة المرور", layout="centered")
load_css(pathlib.Path("styles/style.css"))

st.title("استعادة كلمة المرور")
email = st.text_input("البريد الإلكتروني")
if st.button("إرسال رابط إعادة التعيين"):
    if not email:
        st.warning("يرجى إدخال البريد الإلكتروني المسجل.")
    else:
        supabase = create_client(st.secrets["supabase"]["url"],
                                 st.secrets["supabase"]["anon_key"])
        try:
            supabase.auth.reset_password_for_email(
                email,
                options={"redirectTo": st.secrets["supabase"]["redirect_url"]}
            )
            st.success("تم إرسال الرابط، تحقق من بريدك.")
        except Exception as ex:
            st.error("خطأ أثناء إرسال الرابط.")
            st.error(str(ex))
