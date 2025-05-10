import os
import io
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# -------------------- CONFIG --------------------
DOCUMENT_ID = "GOOGLE DOC DOCUMENT ID TO BE PLACED HERE FOR THE COVER LETTER."
SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/documents']
CREDENTIALS_FILE = "OAUTH 2.0 credentials.json file for the google project we dragging the Cover letter from"

EMAIL = "rstmduran@gmail.com"
PASSWORD = "*********"
SUBJECT = "Jobbmöjlighet"
#Contains email addresses of all kommuns, Along with the kommun names dragged from the domain of the email address.
EMAIL_LIST_PATH = "/Your/Path/To/Emails/emails.txt"

RESUME_PATH = "/Your/Path/To/Resume/RyustemShabanResumeSV.pdf"
FEEDBACK_PATH = "/Your/Path/To/CustomerFeedbacks/Customer_Feedbacks.pdf"

BODY_TEMPLATE = """\
Your body for the email.
"""
# -------------------------------------------------

def authenticate_google():
    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, scopes=SCOPES)
    creds = flow.run_local_server(port=0)
    drive_service = build('drive', 'v3', credentials=creds)
    docs_service = build('docs', 'v1', credentials=creds)
    return drive_service, docs_service

def replace_name_in_doc(docs_service, current_name, previous_name=None):
    target = previous_name if previous_name else "Järfälla"
    requests = [{
        "replaceAllText": {
            "containsText": {"text": target, "matchCase": True},
            "replaceText": current_name
        }
    }]
    docs_service.documents().batchUpdate(documentId=DOCUMENT_ID, body={"requests": requests}).execute()

def export_to_pdf(drive_service, file_id, output_filename):
    request = drive_service.files().export_media(fileId=file_id, mimeType='application/pdf')
    with open(output_filename, 'wb') as f:
        f.write(request.execute())

def attach_file(msg, file_path, display_name=None):
    with open(file_path, 'rb') as f:
        part = MIMEApplication(f.read(), _subtype='pdf')
        part.add_header('Content-Disposition', 'attachment', filename=display_name or os.path.basename(file_path))
        msg.attach(part)

def send_email(recipient, name, pdf_path):
    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = recipient
    msg['Subject'] = SUBJECT

    # Add personalized body
    msg.attach(MIMEText(BODY_TEMPLATE.format(name=name), 'plain'))

    # Attach files
    attach_file(msg, RESUME_PATH)
    attach_file(msg, FEEDBACK_PATH)
    attach_file(msg, pdf_path, "PersonligtBrev.pdf")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)
            print(f"✅ Email sent to {recipient}")
    except Exception as e:
        print(f"❌ Failed to send to {recipient}: {e}")

def main():
    drive_service, docs_service = authenticate_google()
    last_name = None

    with open(EMAIL_LIST_PATH, 'r') as file:
        entries = [line.strip() for line in file if line.strip()]

    for entry in entries:
        try:
            email, name = entry.split(",", 1)
            email, name = email.strip(), name.strip()
            pdf_filename = f"{name}_cover_letter.pdf"

            replace_name_in_doc(docs_service, current_name=name, previous_name=last_name)
            export_to_pdf(drive_service, DOCUMENT_ID, pdf_filename)
            send_email(email, name, pdf_filename)

            os.remove(pdf_filename)
            last_name = name  # Update for next iteration

        except Exception as e:
            print(f"⚠️ Error processing '{entry}': {e}")

if __name__ == "__main__":
    main()
