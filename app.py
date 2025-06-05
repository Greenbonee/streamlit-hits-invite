import streamlit as st
import pandas as pd
import requests
# Streamlit app to invite students to HITS using a CSV file
# Ensure you have the required libraries installed:
# pip install streamlit pandas requests

API_URL = "https://datapipes.api.hits.unimetaverse.net/v1/org/cef7e730-f50c-4a2d-9827-db9adc2b1da0/user/invite"
# Replace with your actual API URL
DEFAULT_DOMAIN = "Training"
DEFAULT_ROLE = "Data User"
# Constants for API interaction
ORG_ID = "cef7e730-f50c-4a2d-9827-db9adc2b1da0"
# Replace with your actual organization ID

st.title("📧 Invite Students to HITS")
st.markdown("""
This app allows you to invite students to the HITS platform by uploading a CSV file containing their email addresses.
The CSV file should have a column named `email` with the students' email addresses.
""")

access_token = st.text_input("Enter your access token", type="password")

uploaded_file = st.file_uploader("Upload CSV File with Student Emails", type="csv")

if uploaded_file and access_token:
    df = pd.read_csv(uploaded_file)

    if 'email' not in df.columns:
        st.error("CSV must have a column named 'email'.")
    else:
        if st.button("Invite Students"):
            results = []
            for idx, row in df.iterrows():
                email = str(row['email']).strip()
                first_name = str(row['first_name']) if 'first_name' in df.columns else ""
                last_name = str(row['last_name']) if 'last_name' in df.columns else ""

                payload = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "role_key": DEFAULT_ROLE,
                    "domain_key": DEFAULT_DOMAIN,
                    "expiration_in_days": 7,
                    "should_reinvite": False,
                    "invite_types": ["PASSWORD"]
                }

                headers = {
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json"
                }

                try:
                    response = requests.post(API_URL, json=payload, headers=headers)
                    if response.status_code == 200:
                        results.append((email, "✅ Success"))
                    elif response.status_code == 422:
                    # Parse and show validation errors
                        errors = response.json().get("detail", [])
                        error_msgs = "; ".join([err.get("msg", "Unknown error") for err in errors])
                        results.append((email, f"❌ Validation Error - {error_msgs}"))
                    else:
                        results.append((email, f"❌ Failed - {response.status_code}: {response.text}"))
                except Exception as e:
                    results.append((email, f"❌ Error - {str(e)}"))

            st.write("### Results")
            for email, result in results:
                st.write(f"{email}: {result}")