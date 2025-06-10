# 📧 HITS Student Invitation App

This is a simple Streamlit web application to invite students to the [HITS platform](https://datapipes.api.hits.unimetaverse.net) using a CSV file.

---

## 🚀 Features

- Upload a CSV file containing student emails and names
- Invite students using the HITS API
- Shows success/failure status for each invite
- Handles validation errors gracefully
- Summarizes invite results (Success, Failures, Skipped)

---

## 📂 CSV Format

Make sure your CSV file includes the following columns:

```csv
email,first_name,last_name
student1@example.com,John,Doe
student2@example.com,Jane,Smith

🛠 Requirements

Python 3.7+
Streamlit
pandas and requests libraries
A valid Bearer Token (provided by HITS)
💻 How to Run Locally

Clone this repository
git clone https://github.com/Greenbonee/streamlit-hits-invite
cd hits-invite-app
Install dependencies
pip install -r requirements.txt
If you don’t have a requirements.txt, use this:

pip install streamlit pandas requests
Run the app
streamlit run app.py
Use the App
Enter your access token
Upload the CSV file
Click "Invite Students"
View results directly on screen
🔐 Access Token

This app requires a valid Bearer token to authorize with the HITS API. If you don’t have one, please contact your admin or refer to the documentation provided during the SIT Academic Retreat.

🙌 Acknowledgements

Built with Streamlit
Powered by the HITS API at UniMetaverse