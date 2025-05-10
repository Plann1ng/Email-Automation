# Email-Automation
Email Automation script for job applications.

# 📬 Automated Job Application Email Sender

This project is a Python-based tool to automate the process of sending personalized job application emails. It dynamically edits a Google Docs-based cover letter for each recipient, converts it to PDF, and sends it along with a resume and customer feedback file via Gmail.

---

## 🚀 Features

- ✅ Personalized email body with recipient name
- ✅ Dynamic replacement of "Järfälla" in a Google Docs template
- ✅ PDF export of edited Google Doc
- ✅ Attachments:
  - Resume (static)
  - Customer feedback (static)
  - Customized cover letter (dynamic)
- ✅ Gmail SMTP integration
- ✅ Handles hundreds of recipients from a single file

---

## 📁 Folder Structure

  project-root/<br>
 │<br>├── send_emails.py # Main script<br>├── emails2.txt # List of recipients: email,name<br>├── RyustemShabanResumeSV.pdf # Resume attachment<br>├── Customer_Feedbacks.pdf # Feedback attachment<br>├── client_secret_*.json # Google API credentials<br>└── README.md<br>


---

## 📋 Prerequisites

- Python 3.7+
- A Gmail account with **App Password enabled**
- A Google Docs cover letter template (shared with your account)

### 🛠 Install Python packages:

```bash
pip3 install --break-system-packages google-auth google-auth-oauthlib google-api-python-client
```



## 🧠 Setup Instructions

### 1. Enable APIs in Google Cloud Console

Go to Google Cloud Console

Create a new project

Enable these APIs:

Google Docs API

Google Drive API

### 2. Create OAuth Credentials

Go to APIs & Services > Credentials

Click "Create Credentials" → "OAuth Client ID"

Choose Desktop App

Download the JSON file and rename it to client_secret.json

Move it to your project folder

### 3. Add Yourself as a Test User

On the OAuth Consent Screen, under Test Users, add your Gmail address.

## ✏️ Format of emails.txt

Each line contains:

pgsql
CopyEdit
email_address,name
Example:

graphql
CopyEdit
ryustem@example.com,Ryustem
stockholm@example.com,Stockholm
▶️ How to Run

bash
CopyEdit
python3 send_emails.py
You will be prompted to authenticate with your Google account the first time. A browser will open. Select your account and approve access.

## 🛡 Security Notes

This project uses a Gmail App Password to send mail securely.

Your Google Docs are edited in-place — no additional copies are created.

Emails are sent over SSL using Gmail’s SMTP server (smtp.gmail.com on port 465).

## 📦 Optional Improvements

Add HTML email support

Log sent emails to a CSV file

Retry failed attempts

Store PDFs in a sent_pdfs/ folder

Auto-skip duplicates

