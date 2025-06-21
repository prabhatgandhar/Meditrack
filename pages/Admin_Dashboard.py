import streamlit as st
import pandas as pd
from utils.db import get_all_data

st.title("Admin Dashboard")

data = pd.DataFrame(get_all_data())

# Remove OPD or irrelevant columns if any
columns_to_drop = [col for col in data.columns if "opd" in col.lower()]
data.drop(columns=columns_to_drop, inplace=True)

# Reorder if needed
desired_order = ["name", "email", "unique_code", "ipd_count", "beneficiary_count", "receipts", "penalty_cases", "rsa_patients", "aor_patients", "timestamp"]
data = data[[col for col in desired_order if col in data.columns]]

st.dataframe(data)

if not data.empty:
    csv = data.to_csv(index=False)
    st.download_button("Download CSV", csv, "doctor_entries.csv", mime="text/csv")
else:
    st.info("No entries available.")

