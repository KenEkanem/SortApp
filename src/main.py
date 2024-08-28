from csv_processor import load_guest_data
from qr_code_generator import generate_qr_code
from access_card_creator import create_access_card
from email_sender import send_email_with_attachment
from sheets_updater import update_barcode_in_sheet
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    csv_file = '../data/guests.csv'
    template_file = '../templates/access_card_template.png'
    qr_code_dir = '../qr_codes/'
    access_card_dir = '../access_cards/'
    base_url = 'http://127.0.0.1:5003/checkin-by-barcode'

    # Retrieve SMTP details from environment variables
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = int(os.getenv('SMTP_PORT'))
    smtp_user = os.getenv('SMTP_USER')
    smtp_password = os.getenv('SMTP_PASSWORD')

    # Load guest data from CSV
    guests = load_guest_data(csv_file)
    if guests is None:
        return

    # Ensure directories exist
    if not os.path.exists(qr_code_dir):
        os.makedirs(qr_code_dir)
    if not os.path.exists(access_card_dir):
        os.makedirs(access_card_dir)
    
    # Process each guest
    for index, guest in guests.iterrows():
        guest_name = guest['name']
        guest_id = str(guest['unique_id'])
        guest_email = guest['email']

        qr_code_file = os.path.join(qr_code_dir, f"qr_{guest_id}.png")
        access_card_file = os.path.join(access_card_dir, f"{guest_name.replace(' ', '_')}_access_card.png")

        # Step 1: Generate QR code with a URL that links to the CheckinApp for this user
        qr_code_url = generate_qr_code(guest_id, guest_email, base_url, qr_code_file)

        # Step 2: Post the QR code URL to the barcode section of the Google Sheets
        update_barcode_in_sheet(guest_email, guest_id, qr_code_url)

        # Step 3: Create the access card with the guest's details
        create_access_card(template_file, guest_name, guest_id, qr_code_file, access_card_file)

        # Step 4: Send an email to the guest with the access card attached
        subject = "Your Access Card"
        body = f"Dear {guest_name},\n\nPlease find your access card attached."
        send_email_with_attachment(smtp_server, smtp_port, smtp_user, smtp_password, guest_email, subject, body, access_card_file)

if __name__ == "__main__":
    main()
