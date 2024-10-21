import os
import smtplib
import pickle
import ssl
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email_content import create_email_content  # Ensure this imports the correct function

# Load environment variables from .env file
load_dotenv()

# Load SMTP configuration from environment variables
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT', '465').strip())
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')

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

    return build(api_name, api_version, credentials=creds)

def upload_file_to_drive(service, file_path):
    """Upload a file to Google Drive and return the shareable link."""
    try:
        file_metadata = {'name': os.path.basename(file_path)}
        media = MediaFileUpload(file_path, mimetype='image/png')
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        file_id = file.get('id')

        # Set file permissions to be publicly accessible
        service.permissions().create(fileId=file_id, body={'role': 'reader', 'type': 'anyone'}).execute()

        return f"https://drive.google.com/uc?id={file_id}"
    except Exception as e:
        print(f"Error during file upload: {e}")
        return None

def send_email_with_drive_link(to_email, guest_name, drive_link):
    """Send an email to the guest with the Google Drive link."""
    # Generate the email subject and body using the imported function
    subject, body = create_email_content(guest_name, drive_link)

    # Create the email message
    message = MIMEMultipart()
    message['From'] = "shamsuddeenusmanbooklaunch@fusedtechie.me"
    message['To'] = to_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'html'))

    # Set up SSLContext for secure connection
    context = ssl.create_default_context()

    try:
        # Connect to the SMTP server and send the email
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(message)
        print(f"Email sent successfully to {to_email}.")
    except smtplib.SMTPAuthenticationError:
        print("Authentication failed with the SMTP server. Please check your SMTP credentials.")
    except smtplib.SMTPConnectError:
        print("Failed to connect to the SMTP server. Please check your SMTP server address and port.")
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
    except Exception as e:
        print(f"Failed to send email: {e}")
