import smtplib
from email.message import EmailMessage
import os

def send_email_with_attachment(smtp_server, smtp_port, smtp_user, smtp_password, to_email, subject, body, attachment_file):
    try:
        # Create the email message
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = smtp_user
        msg['To'] = to_email
        msg.set_content(body)
        
        # Attach the file
        with open(attachment_file, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(attachment_file)
            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

        # Send the email
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_user, smtp_password)
            server.send_message(msg)

        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Error sending email: {e}")
