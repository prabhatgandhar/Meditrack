import streamlit as st
from datetime import datetime, timedelta, timezone
from utils.db import get_daily_data, add_data

st.title("Daily Doctor Entry Form")

# Function to allow typing numbers only
def number_input_text(label):
    value = st.text_input(label)
    if value and not value.isdigit():
        st.warning(f"Please enter a valid number for: {label}")
        return None
    return int(value) if value else 0

if 'user_id' not in st.session_state:
    st.error("Please login first!")
else:
    last_entry = get_daily_data(st.session_state['user_id'])
    if last_entry and (datetime.now(timezone.utc) - last_entry['timestamp'] < timedelta(hours=24)):
        st.error("Data locked after 24 hours!")
    else:
        st.subheader("Enter Today's Data:")

        ipd_count = number_input_text("1️⃣ Total IPD for the day (as per HMIS Portal)")
        beneficiary_count = number_input_text("2️⃣ Total number of beneficiaries registered on HMIS Portal")
        receipts = number_input_text("3️⃣ Total receipts amount (₹)")
        penalty_cases = number_input_text("4️⃣ Penalty beneficiaries on patients for treatment delay")
        rsa_patients = number_input_text("5️⃣ Total number of RSA patients in bed (incl. side/emergency/discharge)")
        aor_patients = number_input_text("6️⃣ Out of total RSA, patients against own risk (AOR)")

        # Submit only if all are valid (None not in any)
        if st.button("Submit"):
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
