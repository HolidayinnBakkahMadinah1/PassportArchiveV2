# """
# HomePage.py — Streamlit + Supabase (بدون تحكم للمستخدم في الدور)
# """
# import streamlit as st
# from supabase import create_client, Client
# import streamlit as st, pathlib, os
# from utils import mount_static, load_css, topbar_logo
# from pathlib import Path


# st.set_page_config(page_title="نظام الأرشفة", layout="wide")

# BASE = Path(__file__).parent
# logo_path = BASE / "static" / "LargeLogo.png"
# st.image(str(logo_path), width=200)

# def load_css(filepath):
#     with open(filepath) as f:
#         st.html(f"<style>{f.read()}</style>")

# css_path = pathlib.Path("styles/style.css")
# load_css(css_path)



# st.image("static/LargeLogo.png", width=200)
# topbar_logo("static/LargeLogo.png") 


# # ─── 0) Streamlit page config ────────────────────────────────────────────────

# # ─── 1) Supabase client (anon key from secrets.toml) ─────────────────────────
# url  = st.secrets["supabase"]["url"]
# anon = st.secrets["supabase"]["anon"]
# supabase: Client = create_client(url, anon)
"""
HomePage.py — Streamlit + Supabase (بدون تحكم للمستخدم في الدور)
"""
import streamlit as st
from supabase import create_client, Client
import streamlit as st, pathlib, os
from utils import load_css
from pathlib import Path


st.set_page_config(page_title="نظام الأرشفة", layout="wide")

BASE = Path(__file__).parent
logo_path = BASE / "static" / "LargeLogo.png"
st.image(str(logo_path), width=200)

def load_css(filepath):
    with open(filepath) as f:
        st.html(f"<style>{f.read()}</style>")

css_path = pathlib.Path("styles/style.css")
load_css(css_path)



st.image("static/LargeLogo.png", width=200)
topbar_logo("static/LargeLogo.png") 


# ─── 0) Streamlit page config ────────────────────────────────────────────────

# ─── 1) Supabase client (anon key from secrets.toml) ─────────────────────────
url  = st.secrets["supabase"]["url"]
anon = st.secrets["supabase"]["anon"]
supabase: Client = create_client(url, anon)

# ─── 2) Session-helper functions ─────────────────────────────────────────────
def login(email: str, password: str):
    """
    Sign user in, fetch role from user_roles (default='user'), store in session.
    Shows raw error while debugging.
    """
    try:
        res  = supabase.auth.sign_in_with_password({"email": email, "password": password})
        uid  = res.user.id

        role_res = (
            supabase.table("user_roles")
            .select("role")
            .eq("id", uid)
            .execute()
        )
        role = role_res.data[0]["role"] if role_res.data else "user"

        st.session_state["authentication_status"] = True
        st.session_state["username"]             = email
        st.session_state["user_roles"]           = [role]
        st.rerun()

    except Exception as e:
        st.error(f"فشل الدخول: {e}")          # for production: replace with generic msg

def register(email: str, password: str):
    """
    Create new Supabase Auth user. Role will be added later by admin in dashboard.
    """
    try:
        supabase.auth.sign_up({"email": email, "password": password})
        st.success("تم إنشاء الحساب! يمكنك الآن تسجيل الدخول.", key="")
    except Exception as e:
        st.error(f"حدث خطأ أثناء إنشاء الحساب: {e}")

def logout():
    for k in ("authentication_status", "username", "user_roles"):
        st.session_state.pop(k, None)
    st.rerun()

# ─── 3) Welcome / Auth UI ────────────────────────────────────────────────────

if not st.session_state.get("authentication_status"):
    # Main welcome card
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("أهلاً بك في نظام أرشفة الجوازات والحقائب")
    col_reg, col_log = st.columns(2, gap="large")
    with col_reg:
        if st.button("تسجيل جديد", key="register"):
            st.session_state["auth_mode"] = "register"
    with col_log:
        if st.button("تسجيل الدخول",key="login"):
            st.session_state["auth_mode"] = "login"
    st.markdown("</div>", unsafe_allow_html=True)

    # Auth modal
    if st.session_state.get("auth_mode") in ("login", "register"):
        mode = st.session_state["auth_mode"]
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("إنشاء حساب" if mode == "register" else "تسجيل الدخول")

        email    = st.text_input("البريد الإلكتروني", key=f"email_{mode}")
        password = st.text_input("كلمة المرور", type="password", key=f"pwd_{mode}")

        if mode == "register":
            if st.button("إنشاء الحساب",key="create"):
                register(email, password)
        else:
            if st.button("دخول",key="enter"):
                login(email, password)
        st.markdown("</div>", unsafe_allow_html=True)

# ─── 4) Logged-in navigation ────────────────────────────────────────────────


if st.session_state.get("authentication_status"):        # logged in
    email = st.session_state["username"]
    role  = st.session_state["user_roles"][0]

    st.success(f"مرحباً **{email}** — دورك: **{role}**")
    if st.button("تسجيل الخروج",key="logout"):
        logout()

    st.markdown("---")
    st.subheader("الصفحات المتاحة:")

    # Passport & Bags for all roles
    if role in ("admin", "editor", "user"):
        st.page_link("pages/Passport.py", label=" أرشفة الجوازات")
        st.page_link("pages/Bags.py",     label=" أرشفة الحقائب")

    # Admin-only page
    if role == "admin":
        st.page_link("pages/admin.py", label=" إدارة المسؤول")

else:  # not logged in
    st.info("يرجى تسجيل الدخول لاستخدام النظام.")


