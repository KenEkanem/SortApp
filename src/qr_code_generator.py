import qrcode

def generate_qr_code(guest_id, guest_email, base_url, qr_code_file):
    # Create the URL that the QR code will point to
    qr_code_url = f"{base_url}?email={guest_email}&unique_id={guest_id}"
    
    # Generate the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_code_url)
    qr.make(fit=True)
    
    # Create an image from the QR code instance
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save the image to the specified file
    img.save(qr_code_file)
    
    # Return the URL to be used for other purposes, such as updating Google Sheets
    return qr_code_url
