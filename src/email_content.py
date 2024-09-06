
# email_content.py

def create_email_content(guest_name, drive_link):
    """Generate the email subject and body based on the guest's name and drive link."""
    subject = "E-Access Card: Shamsuddeen Usman Book Launch"
    body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
            <p>Dear {guest_name},</p>
            <p>We are pleased to provide you with your access card for the <strong>Shamsuddeen Usman Book Launch</strong>. Please find the access card via the following link:</p>
            <p style="text-align: center;">
                <a href="{drive_link}" style="color: #ffffff; background-color: #1a73e8; padding: 10px 20px; border-radius: 4px; text-decoration: none; font-weight: bold;">
                    Access Your E-Card Here
                </a>
            </p>
            <p>Event Details:</p>
            <ul>
                <li><strong>Date:</strong> 26th September 2024</li>
                <li><strong>Time:</strong> 10:00 AM</li>
                <li><strong>Venue:</strong> Musa Yaradua Center, Abuja</li>
            </ul>
            <p>Please note that this card admits one and will be active starting from <strong>26th September 2024</strong>.</p>
            <p>We look forward to welcoming you at the event.</p>
            <br>
            <p>Best regards,<br>PPAI Registration Team</p>
        </body>
    </html>
    """
    return subject, body

    return subject, body
