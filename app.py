import streamlit as st
from utils.auth import create_user
from utils.db import get_daily_data, add_data
from datetime import datetime, timedelta, timezone
from utils.firebase_login import firebase_login

FIREBASE_API_KEY = st.secrets["FIREBASE_API_KEY"]  # ✅ Secure key from secrets

st.set_page_config(page_title="Doctor Data System", layout="centered")
st.title("Doctor Data Management System")

# Safety net: clear session if something is wrong
if 'user_id' in st.session_state and not isinstance(st.session_state['user_id'], str):
    st.session_state.clear()

# Helper function: input number using plain text
def number_input_text(label, key):
    value = st.text_input(label, key=key)
    if value and not value.isdigit():
        st.warning(f"Please enter a valid number for: {label}")
        return None
    return int(value) if value else 0

# Show login/signup tabs if user not logged in
if 'user_id' not in st.session_state:
    tab1, tab2 = st.tabs(["Login", "Signup"])

    # --- LOGIN ---
    with tab1:
        st.subheader("Login")

        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            if email and password:
                try:
                    result = firebase_login(email, password, FIREBASE_API_KEY)
                    user_id = result["localId"]
                    st.session_state['user_id'] = user_id
                    st.session_state['email'] = result["email"]  # ✅ Store email

                    # Load doctor name from Firestore
                    from firebase_admin import firestore
                    db = firestore.client()
                    doc = db.collection("doctors").document(user_id).get()
                    st.session_state['doctor_name'] = doc.to_dict().get("name", "") if doc.exists else ""

                    st.success("Logged in successfully!")
                    st.rerun()

                except Exception as e:
                    st.session_state.clear()
                    st.error(f"Login failed: {str(e)}")
            else:
                st.error("Please enter email and password.")

    # --- SIGNUP ---
    with tab2:
        st.subheader("Create a Doctor Account")
        new_email = st.text_input("Email", key="signup_email")
        new_name = st.text_input("Full Name", key="signup_name")
        unique_code = st.text_input("Unique Code", key="signup_code")
        speciality = st.text_input("Speciality", key="signup_speciality")
        facility_name = st.text_input("Facility Name", key="signup_facility")
        phone = st.text_input("Phone Number", key="signup_phone")
        new_password = st.text_input("Password", type="password", key="signup_password")

        if st.button("Create Account"):
            if not all([new_email, new_name, unique_code, speciality, facility_name, phone, new_password]):
                st.error("Please fill out all fields.")
            else:
                try:
                    user_id = create_user(new_email, new_password, new_name)

                    from firebase_admin import firestore
                    db = firestore.client()
                    db.collection("doctors").document(user_id).set({
                        "email": new_email,
                        "name": new_name,
                        "unique_code": unique_code,
                        "speciality": speciality,
                        "facility_name": facility_name,
                        "phone": phone,
                        "created_at": datetime.now()
                    })

                    st.session_state['user_id'] = user_id
                    st.session_state['doctor_name'] = new_name
                    st.session_state['email'] = new_email  # ✅ Store email on signup
                    st.success("Account created successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(str(e))

# --- LOGGED-IN VIEW ---
else:
    doctor_display = st.session_state.get('doctor_name') or st.session_state.get('email', 'Doctor')
    st.success(f"Welcome, {doctor_display}")  # ✅ Show name or fallback to email

    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()

    st.header("📋 Daily Doctor Entry Form")

    last_entry = get_daily_data(st.session_state['user_id'])
    if last_entry and (datetime.now(timezone.utc) - last_entry['timestamp'] < timedelta(hours=24)):
        st.error("You’ve already submitted data in the last 24 hours.")
    else:
        ipd_count = number_input_text("1️⃣ Total IPD for the day (as per HMIS Portal)", key="ipd")
        beneficiary_count = number_input_text("2️⃣ Total number of beneficiaries registered on HMIS Portal", key="beneficiaries")
        receipts = number_input_text("3️⃣ Total receipts amount (₹)", key="receipts")
        penalty_cases = number_input_text("4️⃣ Penalty beneficiaries on patients for treatment delay", key="penalty")
        rsa_patients = number_input_text("5️⃣ Total number of RSA patients in bed (incl. side/emergency/discharge)", key="rsa")
        aor_patients = number_input_text("6️⃣ Out of total RSA, patients against own risk (AOR)", key="aor")

        if st.button("Submit Entry"):
            if None in (ipd_count, beneficiary_count, receipts, penalty_cases, rsa_patients, aor_patients):
                st.error("Please fill all fields correctly before submitting.")
            else:
                add_data(
                    user_id=st.session_state['user_id'],
                    ipd_count=ipd_count,
                    beneficiary_count=beneficiary_count,
                    receipts=receipts,
                    penalty_cases=penalty_cases,
                    rsa_patients=rsa_patients,
                    aor_patients=aor_patients
                )
                st.success("Data saved successfully!")
