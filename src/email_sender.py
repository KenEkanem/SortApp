import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

# Load environment variables from .env file
load_dotenv()

def authenticate_with_google(api_name, api_version, scopes):
    """Authenticate with Google and return a service object."""
    creds = None
    token_file = 'token.pickle'
    
    CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(
                {
                    "installed": {
                        "client_id": CLIENT_ID,
                        "client_secret": CLIENT_SECRET,
                        "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"],
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token"
                    }
                }, scopes
            )
            creds = flow.run_local_server(port=0)
        
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)

    service = build(api_name, api_version, credentials=creds)
    return service

def upload_file_to_drive(service, file_path):
    """Upload a file to Google Drive and return the shareable link."""
    try:
        file_metadata = {'name': os.path.basename(file_path)}
        media = MediaFileUpload(file_path, mimetype='image/png')
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        file_id = file.get('id')
        print(f"File uploaded successfully. File ID: {file_id}")
        
        # Set file permissions to be publicly accessible
        permissions = {
            'role': 'reader',
            'type': 'anyone',
        }
        service.permissions().create(fileId=file_id, body=permissions).execute()

        return f"https://drive.google.com/uc?id={file_id}"
    except Exception as e:
        print(f"Error during file upload: {e}")
        return None

def send_email_with_attachment(to_email, subject, body, attachment_file):
    """Send an email using Plunk's SMTP server with a Google Drive link to the attachment."""
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = int(os.getenv('SMTP_PORT'))
    smtp_user = os.getenv('SMTP_USER')
    smtp_password = os.getenv('SMTP_PASSWORD')

    # Validate SMTP configuration
    if not smtp_server or not smtp_port or not smtp_user or not smtp_password:
        print("SMTP configuration is missing. Please check your .env file.")
        return

    # Validate SMTP configuration
    if not smtp_server or not smtp_port or not smtp_user or not smtp_password:
        raise ValueError("SMTP configuration is missing. Please check your .env file.")

    # Authenticate with Google Drive
    try:
        drive_service = authenticate_with_google('drive', 'v3', ['https://www.googleapis.com/auth/drive.file'])
    except Exception as e:
        print(f"Failed to authenticate with Google Drive: {e}")
        return

    # Upload the access card to Google Drive and get the shareable link
    drive_link = upload_file_to_drive(drive_service, attachment_file)
    if not drive_link:
        print("Failed to upload file to Google Drive. Email not sent.")
        return

    # Create the email message
    message = MIMEMultipart()
    message['From'] = "ppaibooklaunch@fusedtechie.me"
    message['To'] = to_email
    message['Subject'] = subject

    # Attach the email body with the Google Drive link
    body += f"\n\nYou can download your access card from the following link: {drive_link}"
    message.attach(MIMEText(body, 'plain'))

    # Connect to the SMTP server and send the email
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_user, smtp_password)
            server.send_message(message)
        print(f"Email sent successfully to {to_email} using Plunk's SMTP server.")
    except smtplib.SMTPAuthenticationError:
        print("Authentication failed with Plunk's SMTP server. Please check your SMTP credentials.")
    except smtplib.SMTPConnectError:
        print("Failed to connect to Plunk's SMTP server. Please check your SMTP server address and port.")
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
    except Exception as e:
        print(f"Failed to send email: {e}")
