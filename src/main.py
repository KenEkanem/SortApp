import os
from dotenv import load_dotenv
from csv_processor import load_guest_data
from qr_code_generator import generate_qr_code
from access_card_creator import create_access_card
from sheets_updater import update_barcode_in_sheet
from email_sender import send_email_with_drive_link
from email_content import create_email_content
from email_sender import upload_file_to_drive
from email_sender import authenticate_with_google
import pandas as pd

load_dotenv()

def ensure_directory_exists(directory):
    """Ensure the given directory exists, create if it doesn't."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def process_guest(guest, qr_code_dir, access_card_dir, template_file, base_url, drive_service):
    """Process each guest by generating QR code, updating Google Sheets, creating an access card, and sending an email."""
    
    # Ensure guest_name, guest_id, and guest_email are valid strings and not empty
    guest_name = str(guest['name']).strip() if not pd.isna(guest['name']) else 'Guest'
    guest_id = str(guest['unique_id']).strip() if not pd.isna(guest['unique_id']) else 'unknown'
    guest_email = str(guest['email']).strip() if not pd.isna(guest['email']) else None
    color_name = guest.get('xn', 'default')

    if not guest_email:
        print(f"Skipping guest with missing email: {guest}")
        return

    # Define paths for saving the QR code and access card
    qr_code_file = os.path.join(qr_code_dir, f"qr_{guest_id}.png")
    access_card_file = os.path.join(access_card_dir, f"{guest_name.replace(' ', '_')}_access_card.png")

    # Step 1: Generate QR code with a URL that links to the CheckinApp for this user
    qr_code_url = generate_qr_code(guest_id, guest_email, base_url, qr_code_file)

    # Step 2: Post the QR code URL to the barcode section of the Google Sheets
    update_barcode_in_sheet(guest_email, guest_id, qr_code_url)

    # Step 3: Create the access card with the guest's details, including the color code
    create_access_card(template_file, guest_name, guest_id, qr_code_file, color_name, access_card_file)

    # Step 4: Upload the access card to Google Drive and get the shareable link
    drive_link = upload_file_to_drive(drive_service, access_card_file)

    if drive_link:
        # Step 5: Generate email content with the guest's name and Google Drive link
        subject, body = create_email_content(guest_name, drive_link)
        
        # Step 6: Send an email to the guest with the Google Drive link to the access card
        send_email_with_drive_link(guest_email, guest_name, drive_link)

    else:
        print(f"Failed to upload access card for {guest_name}, email not sent.")


def main():
    csv_file = '../data/guests.csv'
    template_file = '../templates/access_card_template.png'
    qr_code_dir = '../qr_codes/'
    access_card_dir = '../access_cards/'
    base_url = 'https://checkinapp.fusedtechie.me/checkin-by-barcode'

    # Load guest data from CSV
    guests = load_guest_data(csv_file)
    if guests is None:
        print("No guests loaded from CSV.")
        return

    # Ensure directories exist
    ensure_directory_exists(qr_code_dir)
    ensure_directory_exists(access_card_dir)

    # Authenticate with Google Drive API
    drive_service = authenticate_with_google('drive', 'v3', ['https://www.googleapis.com/auth/drive.file'])

    # Process each guest
    for _, guest in guests.iterrows():
        process_guest(guest, qr_code_dir, access_card_dir, template_file, base_url, drive_service)

if __name__ == "__main__":
    main()
