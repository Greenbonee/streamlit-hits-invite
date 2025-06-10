import streamlit as st
import pandas as pd
import requests
import time
# Streamlit app to invite students to HITS using a CSV file
# Ensure you have the required libraries installed:
# pip install streamlit pandas requests

API_URL = "https://datapipes.api.hits.unimetaverse.net/catalog/v1/org/cef7e730-f50c-4a2d-9827-db9adc2b1da0/user/invite"
# Default values for domain and role
DOMAIN_KEY = "cef7e730-f50c-4a2d-9827-db9adc2b1da0://training"
ROLE_KEY = "training://role/data_user"
# Constants for API interaction

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
                time.sleep(1)  # Rate limiting to avoid hitting API too fast
                email = str(row['email']).strip()
                if not email:
                    results.append(("N/A", "⚠️ Skipped: Empty email"))
                    continue

                # Safely get names and strip whitespace
                first_name = str(row.get('first_name', '') or '').strip()
                last_name = str(row.get('last_name', '') or '').strip()

                payload = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "role_key": ROLE_KEY,
                    "domain_key": DOMAIN_KEY,
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
                        errors = response.json().get("detail", [])
                        error_msgs = "; ".join([err.get("msg", "Unknown error") for err in errors])
                        results.append((email, f"❌ Validation Error - {error_msgs}"))
                    else:
                        results.append((email, f"❌ Failed - {response.status_code}: {response.text}"))
                except Exception as e:
                    results.append((email, f"❌ Error - {str(e)}"))

            # Output results
            st.write("### ✅ Invite Results")
            success_count = sum(1 for _, r in results if r.startswith("✅"))
            fail_count = sum(1 for _, r in results if r.startswith("❌"))
            skipped_count = sum(1 for _, r in results if r.startswith("⚠️"))

            for email, result in results:
                st.write(f"{email}: {result}")

            st.markdown("---")
            st.write(f"✅ Successful invites: {success_count}")
            st.write(f"❌ Failed invites: {fail_count}")
            st.write(f"⚠️ Skipped rows: {skipped_count}")
