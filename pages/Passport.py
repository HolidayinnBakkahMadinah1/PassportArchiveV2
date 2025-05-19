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

# # ── Auth guard ──
# if not st.session_state.get("authentication_status"):
#     st.warning("يرجى تسجيل الدخول أولاً.")
#     st.stop()
# roles = st.session_state.get("user_roles", [])
# if not any(r in roles for r in ("admin", "editor","user")):
#     st.error("ليس لديك صلاحية الوصول إلى هذه الصفحة.")
#     st.stop()

# # ── UI & logic (unchanged) ──
# st.title("أرشفة الجوازات")
# st.markdown("أدخل معلومات الجواز في الأسفل:")

# conn = st.connection("gsheets", type=GSheetsConnection)
# existing_dataP = conn.read(worksheet="Passports", usecols=list(range(12)), ttl=10)
# existing_dataB = conn.read(worksheet="Bags",      usecols=list(range(5)),  ttl=10)
# existing_dataP = existing_dataP.dropna(how='all')
# existing_dataB = existing_dataB.dropna(how='all')

# bags_list     = existing_dataB.iloc[:, 0].tolist()
# arrival_gates = ["المطار", "القطار", "كيلو ٩"]
# notes_options = ["لا يوجد","متوفى","مفقود","تم إلقاء القبض","تم ترحيلة"]

# with st.form("PassportForm"):
#     Passport_num = st.text_input("رقم جواز السفر*")
#     Barcode      = st.text_input("باركود نسك*")
#     NameEN       = st.text_input("الإسم باللغة الانجليزية*")
#     NameAR       = st.text_input("الإسم باللغة العربية*")
#     DateOfBirth  = st.date_input("تاريخ الميلاد*", value=date(1990,1,1),
#                                  min_value=date(1900,1,1), max_value=date.today())
#     Gender       = st.selectbox("الجنس*", ("Male","Female"))
#     Nationality  = st.selectbox("الجنسية*", ("باكستان","أندونيسيا","أخرى"))
#     if Nationality == "أخرى":
#         Nationality = st.text_input("الرجاء تحديد الجنسية")
#     Bag          = st.selectbox("رقم الحقيبة*", options=bags_list)
#     Arrival_gate = st.selectbox("بوابة الوصول*", options=arrival_gates)
#     Arrival_date = st.date_input("تاريخ الوصول*", value=date.today())
#     Departure_date = st.date_input("تاريخ المغادرة", value=date.today())
#     Notes        = st.selectbox("الملاحظات", notes_options)

#     if st.form_submit_button("تسجيل"):
#         if not Passport_num:
#             st.warning("الرجاء إدخال رقم الجواز."); st.stop()
#         new_row = pd.DataFrame([{
#             "Passport Number": Passport_num,
#             "Barcode": Barcode,
#             "Name in English": NameEN,
#             "Name in Arabic": NameAR,
#             "Date of Birth": DateOfBirth,
#             "Gender": Gender,
#             "Nationality": Nationality,
#             "Bag Number": Bag,
#             "Arrival Gate": Arrival_gate,
#             "Arrival Date": Arrival_date,
#             "Departure Date": Departure_date,
#             "Notes": Notes,
#         }])
#         # new – worksheet + dataframe as keywords:
#         full_df = pd.concat([existing_dataP, new_row], ignore_index=True)
#         # ← use .write() here, not .update()
#         conn.write(full_df, worksheet="Passports")

#         st.success("تم حفظ بيانات الجواز بنجاح!")
# import streamlit as st, pandas as pd, pathlib
# from datetime import date
# from google.oauth2.service_account import Credentials
# import gspread
# from utils import load_css

# st.set_page_config(page_title="جوازات السفر", layout="wide")
# load_css(pathlib.Path("styles/style.css"))

# # ── Auth guard ────────────────────────────────────────────────────────
# if not st.session_state.get("authentication_status"):
#     st.info("يرجى تسجيل الدخول لاستخدام النظام.")
#     st.stop()

# # ── Build a gspread client from secrets ───────────────────────────────
# SCOPES = [
#     "https://www.googleapis.com/auth/spreadsheets",
#     "https://www.googleapis.com/auth/drive",
# ]
# creds = Credentials.from_service_account_info(
#     st.secrets["connections"]["gsheets"], scopes=SCOPES
# )
# gc = gspread.authorize(creds)
# sh = gc.open_by_url(st.secrets["connections"]["gsheets"]["spreadsheet"])
# ws_passports = sh.worksheet("Passports")
# ws_bags      = sh.worksheet("Bags")

# # ── Load existing data into DataFrames (for select boxes etc.) ────────
# existing_P = pd.DataFrame(ws_passports.get_all_records())
# existing_B = pd.DataFrame(ws_bags.get_all_records())

# if "Bag Number" in existing_B.columns:
#     bags_list = existing_B["Bag Number"].dropna().tolist()
# else:
#     bags_list = []       

# arrival_gates = ["المطار", "القطار", "كيلو ٩"]
# notes_options = ["لا يوجد", "متوفى", "مفقود", "تم إلقاء القبض", "تم ترحيله"]

# st.title("أرشفة الجوازات")
# with st.form("PassportForm"):
#     Passport_num   = st.text_input("رقم جواز السفر*")
#     Barcode        = st.text_input("باركود نسك*")
#     NameEN         = st.text_input("الإسم بالإنجليزية*")
#     NameAR         = st.text_input("الإسم بالعربية*")
#     DateOfBirth    = st.date_input("تاريخ الميلاد*", value=date(1990,1,1),
#                                    min_value=date(1900,1,1), max_value=date.today())
#     Gender         = st.selectbox("الجنس*", ("Male", "Female"))
#     Nationality    = st.selectbox("الجنسية*", ("باكستان","أندونيسيا","أخرى"))
#     if Nationality == "أخرى":
#         Nationality = st.text_input("الرجاء تحديد الجنسية")

#     Bag            = st.selectbox("رقم كشف الحقيبة", options=bags_list)
#     Arrival_gate   = st.selectbox("بوابة الوصول*", options=arrival_gates)
#     Arrival_date   = st.date_input("تاريخ الوصول*", value=date.today())
#     Departure_date = st.date_input("تاريخ المغادرة", value=date.today())
#     Notes          = st.selectbox("الملاحظات", notes_options)

#     if st.form_submit_button("تسجيل"):
#         if not Passport_num:
#             st.warning("الرجاء إدخال رقم الجواز")
#             st.stop()

#         # build & append the row
#         new_row = [
#             Passport_num, Barcode, NameEN, NameAR,
#             DateOfBirth.strftime("%Y-%m-%d"),
#             Gender, Nationality, Bag, Arrival_gate,
#             Arrival_date.strftime("%Y-%m-%d"),
#             Departure_date.strftime("%Y-%m-%d"),
#             Notes,
#         ]
#         ws_passports.append_row(new_row, value_input_option="USER_ENTERED")
#         st.success("تم حفظ بيانات الجواز بنجاح!")
# pages/Passport.py ───────────────────────────────────────────────────
#-------------------v2.2--------------------
# import streamlit as st, pandas as pd, pathlib, re
# from datetime import date, datetime
# from google.oauth2.service_account import Credentials
# import gspread, pytesseract
# from PIL import Image
# from utils import load_css, get_gsheets_client, parse_mrz

# st.set_page_config(page_title="جوازات السفر", layout="wide")
# load_css(pathlib.Path("styles/style.css"))

# # ── auth guard ───────────────────────────────────────────────────────
# if not st.session_state.get("authenticated"):
#     st.info("يرجى تسجيل الدخول لاستخدام النظام.")
#     st.stop()

# user_email = st.session_state["user_email"]

# # ── Google-sheet handles ─────────────────────────────────────────────
# gc, sh = get_gsheets_client()
# ws_passports = sh.worksheet("Passports")
# ws_bags      = sh.worksheet("Bags")

# # ── cached existing passports for duplicate check ───────────────────
# @st.cache_data(ttl=120)
# def get_existing_passports():
#     df = pd.DataFrame(ws_passports.get_all_records())
#     return set(df["Passport Number"].astype(str))

# existing_numbers = get_existing_passports()

# # ── bags list for selectbox ──────────────────────────────────────────
# bags_df = pd.DataFrame(ws_bags.get_all_records())
# bags_list = bags_df["Bag Number"].dropna().tolist() if "Bag Number" in bags_df else []

# # ── OCR capture / upload ─────────────────────────────────────────────
# st.title("📄 إضافة معلومات الجواز")

# img_file = st.camera_input("التقط صورة الجواز") or st.file_uploader(
#     "أو قم برفع صورة", type=["jpg", "jpeg", "png"]
# )
# if img_file:
#     img = Image.open(img_file)
#     ocr_text = pytesseract.image_to_string(img, lang="ara+eng")
#     mrz_fields = parse_mrz(ocr_text)
#     if mrz_fields:
#         st.success("✅ تم استخراج البيانات آليًا، يمكنك التعديل قبل الحفظ.")
#         st.session_state.update(
#             passport_no=mrz_fields["passport"],
#             dob=mrz_fields["dob"],
#             gender=mrz_fields["gender"],
#             nationality=mrz_fields["nat"],
#         )
#     else:
#         st.warning("لم أستطع التعرف على معلومات MRZ، يرجى الإدخال يدويًا.")

# # ── passport entry form ──────────────────────────────────────────────
# with st.form("pass_form", clear_on_submit=False):
#     bag_no       = st.text_input("رقم الحقيبة*", key="bag_no")
#     passport_no  = st.text_input("رقم الجواز*",  key="passport_no")
#     dob          = st.text_input("تاريخ الميلاد (YYYY-MM-DD)*", key="dob")
#     gender       = st.selectbox("الجنس*", ["M", "F"], key="gender")
#     nationality  = st.text_input("الجنسية*", key="nationality")
#     barcode      = st.text_input("باركود نسك (اختياري)")
#     name_en      = st.text_input("الاسم بالإنجليزية (اختياري)")
#     name_ar      = st.text_input("الاسم بالعربية (اختياري)")
#     arr_gate     = st.selectbox("بوابة الوصول*", ["المطار","القطار","كيلو ٩"])
#     arr_date     = st.date_input("تاريخ الوصول*", value=date.today())
#     dep_date     = st.date_input("تاريخ المغادرة", value=date.today())
#     notes        = st.text_input("ملاحظات")
#     submitted    = st.form_submit_button("حفظ السجل")

# if submitted:
#     if not (bag_no and passport_no and dob and nationality):
#         st.warning("الرجاء تعبئة الحقول الإلزامية (رقم الحقيبة، رقم الجواز، تاريخ الميلاد، الجنسية).")
#         st.stop()

#     if passport_no.strip() in existing_numbers:
#         st.warning("🚫 هذا الجواز مسجل مسبقًا ولا يمكن تكراره.")
#         st.stop()

#     row = [
#         datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         bag_no, passport_no, dob, gender, nationality,
#         barcode, name_en, name_ar,
#         arr_gate, arr_date.strftime("%Y-%m-%d"),
#         dep_date.strftime("%Y-%m-%d"), notes,
#         user_email,   # log who added
#     ]
#     ws_passports.append_row(row, value_input_option="USER_ENTERED")
#     st.success("✅ تم حفظ السجل بنجاح!")
#     existing_numbers.add(passport_no.strip())        # update cache
#     # clear fields except bag_no
#     for k in ("passport_no","dob","gender","nationality","barcode","name_en","name_ar","notes"):
#         st.session_state[k] = ""
#---------------------v2.3--------------------
# pages/Passport.py
# pages/Passport.py
# import streamlit as st, pandas as pd, pathlib
# from datetime import date
# from google.oauth2.service_account import Credentials
# import gspread, pytesseract
# from PIL import Image
# from utils import load_css

# # 1) page setup
# st.set_page_config(page_title="جوازات السفر", layout="wide")
# load_css(pathlib.Path("styles/style.css"))

# # 2) auth guard
# if not st.session_state.get("authenticated"):
#     st.info("يرجى تسجيل الدخول لاستخدام النظام.")
#     st.stop()

# # 3) GSheets client
# SCOPES = [
#     "https://www.googleapis.com/auth/spreadsheets",
#     "https://www.googleapis.com/auth/drive",
# ]
# creds = Credentials.from_service_account_info(
#     st.secrets["connections"]["gsheets"],
#     scopes=SCOPES,
# )
# gc = gspread.authorize(creds)
# sh = gc.open_by_url(st.secrets["connections"]["gsheets"]["spreadsheet"])
# ws_passports = sh.worksheet("Passports")
# ws_bags      = sh.worksheet("Bags")

# # 4) helper to parse MRZ — very minimal, tweak as needed:
# def parse_mrz(text: str):
#     # split out the last two lines of OCR output (MRZ zone)
#     lines = [l for l in text.splitlines() if l.strip()]
#     if len(lines) < 2:
#         return None
#     l1, l2 = lines[-2], lines[-1]
#     # passport number = first 9 chars of line2
#     passport = l2[0:9].replace('<','').strip()
#     dob     = l2[13:19]      # YYMMDD
#     gender  = l2[20]         # M/F/<
#     nat     = l2[10:13]      # three-letter code
#     # convert YYMMDD → YYYY-MM-DD
#     try:
#         yy,mm,dd = int(dob[0:2]), int(dob[2:4]), int(dob[4:6])
#         year = 1900 + yy if yy > 30 else 2000 + yy
#         dob_fmt = f"{year:04d}-{mm:02d}-{dd:02d}"
#     except:
#         dob_fmt = ""
#     return {
#         "passport": passport,
#         "dob":       dob_fmt,
#         "gender":   "Male" if gender in ("M","m") else "Female",
#         "nat":      {"PAK":"باكستان","IDN":"أندونيسيا"}.get(nat, "")
#     }

# # 5) pull current bag list
# existing_B = pd.DataFrame(ws_bags.get_all_records())
# bags_list = (
#     existing_B["Bag Number"].dropna().tolist()
#     if "Bag Number" in existing_B.columns else []
# )

# arrival_gates = ["المطار", "القطار", "كيلو ٩"]
# notes_options = ["لا يوجد", "متوفى", "مفقود", "تم إلقاء القبض", "تم ترحيله"]

# st.title("أرشفة الجوازات")

# # ───────────────────────────────────────────────────────────
# # OCR capture / upload step
# img = st.camera_input("التقط صورة الجواز") or st.file_uploader(
#     "أو قم برفع صورة الجواز", type=["jpg","jpeg","png"]
# )
# if img:
#     pil = Image.open(img)
#     raw = pytesseract.image_to_string(pil, lang="ara+eng")  # OCR-B model
#     fields = parse_mrz(raw)
#     if fields:
#         st.success("✅ تم استخراج البيانات آليًا، يمكنك التعديل قبل الحفظ.")
#         # push into session_state so form shows them
#         st.session_state["passport_no"]  = fields["passport"]
#         st.session_state["dob"]          = fields["dob"]
#         st.session_state["gender"]       = fields["gender"]
#         st.session_state["nationality"]  = fields["nat"]
#     else:
#         st.warning("لم أستطع التعرف على بيانات MRZ، الرجاء الإدخال يدويًا.")

# # ───────────────────────────────────────────────────────────
# # the entry form — keyed to session_state for defaults
# with st.form("PassportForm", clear_on_submit=False):
#     Bag           = st.selectbox("رقم كشف الحقيبة*", options=bags_list, key="bag")
#     Passport_num  = st.text_input("رقم جواز السفر*", key="passport_no")
#     DateOfBirth  = st.date_input("تاريخ الميلاد*", value=date(1990,1,1),min_value=date(1900,1,1), max_value=date.today())
#     Gender        = st.selectbox("الجنس*", ["Male","Female"], key="gender")
#     Nationality   = st.text_input("الجنسية*", key="nationality")

#     # optional fields
#     Barcode       = st.text_input("باركود نسك (اختياري)", key="barcode")
#     NameEN        = st.text_input("الاسم بالإنجليزية (اختياري)", key="name_en")
#     NameAR        = st.text_input("الاسم بالعربية (اختياري)", key="name_ar")

#     Arrival_gate   = st.selectbox("بوابة الوصول*", options=arrival_gates, key="arrival_gate")
#     Arrival_date   = st.date_input("تاريخ الوصول*", value=date.today(), key="arrival_date")
#     Departure_date = st.date_input("تاريخ المغادرة", value=date.today(), key="departure_date")
#     Notes          = st.selectbox("الملاحظات", notes_options, key="notes")

#     submitted = st.form_submit_button("تسجيل")

# if submitted:
#     # required checks
#     if not (Bag and Passport_num and DateOfBirth and Nationality):
#         st.warning("الرجاء تعبئة جميع الحقول الإلزامية.")
#         st.stop()

#     # duplicate check
#     existing_P = pd.DataFrame(ws_passports.get_all_records())
#     if Passport_num.strip() in existing_P["Passport Number"].astype(str).tolist():
#         st.warning("🚫 هذا الجواز مسجل مسبقًا.")
#         st.stop()

#     # append the row
#     row = [
#         Passport_num.strip().upper(),
#         Barcode, NameEN, NameAR,
#         DateOfBirth, Gender, Nationality,
#         Bag, Arrival_gate,
#         Arrival_date.strftime("%Y-%m-%d"),
#         Departure_date.strftime("%Y-%m-%d"),
#         Notes,
#         st.session_state["user_email"],    # who added
#     ]
#     ws_passports.append_row(row, value_input_option="USER_ENTERED")
#     st.success("✅ تم حفظ بيانات الجواز بنجاح!")

#     # clear all except bag
#     for k in ("passport_no","dob","gender","nationality",
#               "barcode","name_en","name_ar","notes"):
#         st.session_state[k] = ""
#---------------------------v4-------------------------------
# pages/Passport.py
# import os
# import shutil
# import pytesseract

# # ───────────────────────────────────────────────────
# # ① point Tesseract at your tessdata folder:
# os.environ["TESSDATA_PREFIX"] = "/Users/faisal/myproject"

# # ② locate the Homebrew‐installed tesseract binary
# tess_path = shutil.which("tesseract") or "/opt/homebrew/bin/tesseract"
# pytesseract.pytesseract.tesseract_cmd = tess_path
# # ───────────────────────────────────────────────────

# # now you can import the rest
# from PIL import Image
# import streamlit as st
# import pandas as pd
# import pathlib
# from datetime import date
# from google.oauth2.service_account import Credentials
# import gspread
# from utils import load_css
# # tell pytesseract where the binary is:
# pytesseract.pytesseract.tesseract_cmd = pytesseract_cmd

# st.set_page_config(page_title="جوازات السفر", layout="wide")
# load_css(pathlib.Path("styles/style.css"))

# # ── Auth guard ────────────────────────────────────────────────────────
# if not st.session_state.get("authenticated"):
#     st.info("يرجى تسجيل الدخول لاستخدام النظام.")
#     st.stop()

# # ── Build a gspread client from secrets ───────────────────────────────
# SCOPES = [
#     "https://www.googleapis.com/auth/spreadsheets",
#     "https://www.googleapis.com/auth/drive",
# ]
# creds = Credentials.from_service_account_info(
#     st.secrets["connections"]["gsheets"],
#     scopes=SCOPES,
# )
# gc = gspread.authorize(creds)
# sh = gc.open_by_url(st.secrets["connections"]["gsheets"]["spreadsheet"])
# ws_passports = sh.worksheet("Passports")
# ws_bags      = sh.worksheet("Bags")

# # ── Load existing data into DataFrames (for select boxes etc.) ────────
# existing_P = pd.DataFrame(ws_passports.get_all_records())
# existing_B = pd.DataFrame(ws_bags.get_all_records())

# bags_list = (
#     existing_B["Bag Number"].dropna().tolist()
#     if "Bag Number" in existing_B.columns else []
# )

# arrival_gates = ["المطار", "القطار", "كيلو ٩"]
# notes_options = ["لا يوجد", "متوفى", "مفقود", "تم إلقاء القبض", "تم ترحيله"]

# st.title("📄 أرشفة الجوازات")

# # ── OCR capture & upload ──────────────────────────────────────────────
# img_file = (
#     st.camera_input("📷 التقط صورة الجواز (اختياري)")
#     or st.file_uploader("أو قم برفع صورة الجواز", type=["jpg", "jpeg", "png"])
# )

# if img_file:
#     pil = Image.open(img_file)
#     # run Tesseract with both Arabic + English models:
#     raw = pytesseract.image_to_string(pil, lang="ara+eng")
#     # Pull out MRZ–style fields or fallback to full-text parse…
#     # (you can plug in your parse_mrz() here)
#     st.session_state["Passport_num"] = ""
#     st.session_state["DateOfBirth"]  = ""
#     st.session_state["Gender"]       = ""
#     st.session_state["Nationality"]  = ""
#     # Provide feedback:
#     st.success("✅ تم استخراج النصّ من الصورة. الرجاء استكمال أو تعديل الحقول أدناه.")

# # ── Passport entry form ────────────────────────────────────────────────
# with st.form("PassportForm", clear_on_submit=False):
#     # if OCR set any defaults, they’ll populate these fields:
#     Passport_num   = st.text_input("رقم جواز السفر*", key="Passport_num")
#     Barcode        = st.text_input("باركود نسك*",        key="Barcode")
#     NameEN         = st.text_input("الإسم بالإنجليزية*", key="NameEN")
#     NameAR         = st.text_input("الإسم بالعربية*",    key="NameAR")
#     DateOfBirth    = st.date_input(
#         "تاريخ الميلاد*",
#         value=date(1990,1,1),
#         min_value=date(1900,1,1),
#         max_value=date.today(),
#         key="DateOfBirth"
#     )
#     Gender         = st.selectbox(
#         "الجنس*",
#         ("Male","Female"),
#         index=0,
#         key="Gender"
#     )
#     Nationality    = st.selectbox(
#         "الجنسية*",
#         ("باكستان","أندونيسيا","أخرى"),
#         index=0,
#         key="Nationality"
#     )
#     if st.session_state["Nationality"] == "أخرى":
#         st.session_state["Nationality"] = st.text_input(
#             "الرجاء تحديد الجنسية", key="Nationality_manual"
#         )

#     Bag            = st.selectbox("رقم كشف الحقيبة*", options=bags_list, key="Bag")
#     Arrival_gate   = st.selectbox("بوابة الوصول*", options=arrival_gates, key="Arrival_gate")
#     Arrival_date   = st.date_input("تاريخ الوصول*", value=date.today(), key="Arrival_date")
#     Departure_date = st.date_input("تاريخ المغادرة", value=date.today(), key="Departure_date")
#     Notes          = st.selectbox("الملاحظات", notes_options, key="Notes")

#     submitted = st.form_submit_button("تسجيل")
#     if submitted:
#         if not st.session_state["Passport_num"]:
#             st.warning("الرجاء إدخال رقم الجواز")
#             st.stop()

#         # append the row to Google Sheets:
#         new_row = [
#             st.session_state["Passport_num"].upper(),  # ensure uppercase
#             st.session_state["Barcode"],
#             st.session_state["NameEN"],
#             st.session_state["NameAR"],
#             st.session_state["DateOfBirth"].strftime("%Y-%m-%d"),
#             st.session_state["Gender"],
#             st.session_state["Nationality"],
#             st.session_state["Bag"],
#             st.session_state["Arrival_gate"],
#             st.session_state["Arrival_date"].strftime("%Y-%m-%d"),
#             st.session_state["Departure_date"].strftime("%Y-%m-%d"),
#             st.session_state["Notes"],
#             st.session_state["username"],  # who added the entry
#         ]
#         ws_passports.append_row(new_row, value_input_option="USER_ENTERED")
#         st.success("✅ تم حفظ بيانات الجواز بنجاح!")
#--------------------------------------------------------

# pages/Passport.py
# pages/Passport.py
# import streamlit as st
# import pandas as pd
# import pathlib
# from datetime import date
# from google.oauth2.service_account import Credentials
# import gspread
# from utils import load_css

# # ─── 1) إعداد الصفحة ────────────────────────────────────────────────
# st.set_page_config(page_title="جوازات السفر", layout="wide")
# load_css(pathlib.Path("styles/style.css"))

# # ─── 2) التحقق من تسجيل الدخول ─────────────────────────────────────
# if not st.session_state.get("authenticated"):
#     st.info("يرجى تسجيل الدخول لاستخدام النظام.")
#     st.stop()

# current_user = st.session_state["user_email"]

# # ─── 3) الاتصال بجوجل شيتس ─────────────────────────────────────────
# SCOPES = [
#     "https://www.googleapis.com/auth/spreadsheets",
#     "https://www.googleapis.com/auth/drive",
# ]
# creds = Credentials.from_service_account_info(
#     st.secrets["connections"]["gsheets"], scopes=SCOPES
# )
# gc = gspread.authorize(creds)
# sh = gc.open_by_url(st.secrets["connections"]["gsheets"]["spreadsheet"])
# ws_passports = sh.worksheet("Passports")
# ws_bags      = sh.worksheet("Bags")

# passports_df = pd.DataFrame(ws_passports.get_all_records())
# bags_df      = pd.DataFrame(ws_bags.get_all_records())

# bags_list = bags_df["Bag Number"].dropna().tolist() if "Bag Number" in bags_df else []
# arrival_gates = ["المطار", "القطار", "كيلو ٩"]
# notes_options = ["لا يوجد", "متوفى", "مفقود", "تم إلقاء القبض", "تم ترحيله"]

# st.title("أرشفة الجوازات")

# # ─── 4) اختيار الحقيبة + عدّاد دينامى ──────────────────────────────
# selected_bag = st.selectbox("اختر رقم الحقيبة*", bags_list, key="selected_bag")

# def count_passports_for(bag_no: str) -> int:
#     return passports_df[passports_df["Bag Number"] == bag_no].shape[0]

# bag_counter_placeholder = st.empty()
# bag_counter_placeholder.info(
#     f"📦 الجوازات المسجَّلة لهذه الحقيبة: **{count_passports_for(selected_bag)}**"
# )

# # ─── 5) نموذج الإدخال ──────────────────────────────────────────────
# with st.form("PassportForm", clear_on_submit=False):

#     Passport_num = st.text_input("رقم جواز السفر*", key="passport_no").upper()

#     DateOfBirth  = st.date_input(
#         "تاريخ الميلاد*",
#         value=date(1990, 1, 1),
#         min_value=date(1900, 1, 1),
#         max_value=date.today(),
#     )

#     Gender = st.selectbox("الجنس*", ("Male", "Female"), key="gender")

#     nat_choice = st.selectbox("الجنسية*", ("باكستان", "أندونيسيا", "أخرى"), key="nat_choice")
#     if nat_choice == "أخرى":
#         Nationality = st.text_input("الرجاء تحديد الجنسية*", key="nationality")
#     else:
#         Nationality = nat_choice

#     # حقول اختيارية
#     Barcode = st.text_input("باركود نسك (اختياري)", key="barcode")
#     NameEN  = st.text_input("الاسم بالإنجليزية (اختياري)", key="name_en")
#     NameAR  = st.text_input("الاسم بالعربية (اختياري)",   key="name_ar")

#     Arrival_gate   = st.selectbox("بوابة الوصول*", arrival_gates, key="arrival_gate")
#     Arrival_date   = st.date_input("تاريخ الوصول*", value=date.today(), key="arrival_date")
#     Departure_date = st.date_input("تاريخ المغادرة", value=date.today(), key="departure_date")
#     Notes          = st.selectbox("الملاحظات", notes_options, key="notes")

#     submitted = st.form_submit_button("تسجيل")

# # ─── 6) عند الحفظ ──────────────────────────────────────────────────
# if submitted:

#     # تحقق من الحقول الإلزامية
#     if not (selected_bag and Passport_num and DateOfBirth and Nationality):
#         st.warning("الرجاء تعبئة جميع الحقول الإلزامية.")
#         st.stop()

#     # منع التكرار
#     if Passport_num in passports_df["Passport Number"].astype(str).tolist():
#         st.warning(" هذا الجواز مسجَّل مسبقًا.")
#         st.stop()

#     # إضافة الصفّ
#     row = [
#         Passport_num,
#         Barcode, NameEN, NameAR,
#         DateOfBirth.strftime("%Y-%m-%d"),
#         Gender, Nationality,
#         selected_bag, Arrival_gate,
#         Arrival_date.strftime("%Y-%m-%d"),
#         Departure_date.strftime("%Y-%m-%d"),
#         Notes,
#         current_user,
#     ]
#     ws_passports.append_row(row, value_input_option="USER_ENTERED")

#     st.success(" تم حفظ بيانات الجواز بنجاح!")

#     # تحديث الـ DataFrame والعدّاد محليًا ثم إعادة تشغيل الصفحة
#     passports_df.loc[len(passports_df)] = {
#         "Passport Number": Passport_num,
#         "Bag Number":      selected_bag,
#     }
#     st.session_state["passport_no"] = ""   # تفريغ الحقل بعد الحفظ
#     st.experimental_rerun()                # يعيد الحساب ويُظهِر العدّاد الجديد
#-------------------------------------------------------------
import streamlit as st, pandas as pd, pathlib
from datetime import date
from google.oauth2.service_account import Credentials
import gspread
from utils import load_css

# ─── page setup & CSS ───────────────────────────────────────────────
st.set_page_config(page_title="جوازات السفر", layout="wide")
load_css(pathlib.Path("styles/style.css"))

# ─── authentication guard ──────────────────────────────────────────
if not st.session_state.get("authenticated"):
    st.info("يرجى تسجيل الدخول لاستخدام النظام.")
    st.stop()

user_email = st.session_state["user_email"]

# ─── G-Sheets connection helpers ───────────────────────────────────
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
creds  = Credentials.from_service_account_info(
    st.secrets["connections"]["gsheets"], scopes=SCOPES
)
gc     = gspread.authorize(creds)
sh     = gc.open_by_url(st.secrets["connections"]["gsheets"]["spreadsheet"])
ws_p   = sh.worksheet("Passports")
ws_b   = sh.worksheet("Bags")

df_p = pd.DataFrame(ws_p.get_all_records())
df_b = pd.DataFrame(ws_b.get_all_records())

bags_list = df_b["Bag Number"].dropna().tolist() if "Bag Number" in df_b else []
arrival_gates = ["المطار", "القطار", "كيلو ٩"]
notes_options  = ["لا يوجد", "متوفى", "مفقود", "تم إلقاء القبض", "تم ترحيله"]

st.title("أرشفة الجوازات")

# ─── bag selector + live counter ────────────────────────────────────
selected_bag = st.selectbox("رقم الحقيبة*", bags_list)
bag_count = df_p[df_p["Bag Number"] == selected_bag].shape[0]
st.info(f"📦 عدد الجوازات المسجَّلة لهذه الحقيبة: **{bag_count}**")

# ─── passport entry form (auto-clears) ─────────────────────────────
with st.form("passport_form", clear_on_submit=True):
    passport_no = st.text_input("رقم جواز السفر*").upper()
    dob         = st.date_input("تاريخ الميلاد*", value=date(1990,1,1),
                                min_value=date(1900,1,1), max_value=date.today())
    gender      = st.selectbox("الجنس*", ["Male","Female"])

    nat_choice  = st.selectbox("الجنسية*", ["باكستان","أندونيسيا","أخرى"])
    nationality = st.text_input("الرجاء تحديد الجنسية") if nat_choice == "أخرى" else nat_choice

    barcode     = st.text_input("باركود نسك (اختياري)")
    name_en     = st.text_input("الاسم بالإنجليزية (اختياري)")
    name_ar     = st.text_input("الاسم بالعربية (اختياري)")

    gate        = st.selectbox("بوابة الوصول*", arrival_gates)
    arr_date    = st.date_input("تاريخ الوصول*", value=date.today())
    dep_date    = st.date_input("تاريخ المغادرة", value=date.today())
    notes       = st.selectbox("الملاحظات", notes_options)

    submitted   = st.form_submit_button("حفظ السجل")

# ─── save logic ─────────────────────────────────────────────────────
if submitted:
    if not passport_no:
        st.error("الرجاء إدخال رقم جواز السفر.")
        st.stop()

    if passport_no in df_p["Passport Number"].astype(str).tolist():
        st.warning("🚫 هذا الجواز مسجَّل مسبقًا.")
        st.stop()

    new_row = [
        passport_no, barcode, name_en, name_ar,
        dob.strftime("%Y-%m-%d"), gender, nationality,
        selected_bag, gate,
        arr_date.strftime("%Y-%m-%d"),
        dep_date.strftime("%Y-%m-%d"),
        notes,
        user_email,                 # SubmittedBy
    ]
    ws_p.append_row(new_row, value_input_option="USER_ENTERED")
    st.success("✅ تم حفظ بيانات الجواز بنجاح!")
    st.rerun() 