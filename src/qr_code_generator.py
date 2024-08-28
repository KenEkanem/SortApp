import qrcode
import requests

# Your Google Apps Script URL
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbx8o0uVWqb809GKNUv7n1i5ESGLR3F8U_vTwLH7rSYlqPs_T0jK6Kj1o-ZXF6iPlEbqig/exec"

def generate_qr_code(user_id, user_email, base_url, output_file):
    # Generate the URL with the user-specific link
    url = f"{base_url}?unique_id={user_id}&email={user_email}"
    
    # Generate the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img.save(output_file)
    
    return url  # Return the URL for posting to Google Sheets

def update_barcode_in_sheet(sheet_id, sheet_name, user_id, qr_code_url):
    # Define the parameters for the POST request
    params = {
        'sheet_id': sheet_id,
        'sheet_name': sheet_name,
        'user_id': user_id,
        'barcode_url': qr_code_url
    }
    
    try:
        # Make the request to the Google Apps Script
        response = requests.post(GOOGLE_SCRIPT_URL, data=params)
        
        if response.status_code == 200:
            print(f"Barcode successfully updated for user ID {user_id}")
        else:
            print(f"Failed to update barcode for user ID {user_id}: {response.status_code}")
    except Exception as e:
        print(f"Error updating barcode: {str(e)}")
