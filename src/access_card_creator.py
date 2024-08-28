from PIL import Image, ImageDraw, ImageFont
import os

def create_access_card(template_file, guest_name, guest_id, qr_code_file, output_file):
    try:
        # Check if files exist
        if not os.path.exists(template_file):
            raise FileNotFoundError(f"Template file not found: {template_file}")
        if not os.path.exists(qr_code_file):
            raise FileNotFoundError(f"QR code file not found: {qr_code_file}")

        # Open the template image
        template = Image.open(template_file)
        draw = ImageDraw.Draw(template)
        
        # Load a font (adjust the path to your font file)
        try:
            font_path = "/home/elysium/.fonts/JetBrainsMonoNLNerdFont-Regular.ttf"  # Font Path
            font = ImageFont.truetype(font_path, 40)
        except IOError:
            print("Font file not found, using default font.")
            font = ImageFont.load_default()
        
        # Convert guest_id to string to avoid issues
        guest_id = str(guest_id).strip()

        # Define positions for name and ID
        name_position = (365, 1520)
        id_position = (363, 1670)

        # Load the QR code image
        qr_img = Image.open(qr_code_file)

        # Define the QR code box area on the template
        qr_top_left = (196, 1029)
        qr_bottom_right = (598, 1433)

        # Calculate QR code size and position
        qr_width = qr_bottom_right[0] - qr_top_left[0]
        qr_height = qr_bottom_right[1] - qr_top_left[1]
        qr_size = min(qr_width, qr_height)

        # Resize the QR code to fit the box
        qr_img = qr_img.resize((qr_size, qr_size))

        # Calculate position to paste the QR code (center it within the box)
        qr_position = (
            qr_top_left[0] + (qr_width - qr_size) // 2,
            qr_top_left[1] + (qr_height - qr_size) // 2
        )

        # Draw text on the image
        print(f"Drawing Name: '{guest_name}' at {name_position}")
        print(f"Drawing ID: '{guest_id}' at {id_position}")
        draw.text(name_position, guest_name, font=font, fill="black")
        draw.text(id_position, guest_id, font=font, fill="black")

        # Paste the QR code onto the template
        template.paste(qr_img, qr_position)

        # Save the final access card
        template.save(output_file)
        print(f"Access card created and saved as {output_file}")
        
    except Exception as e:
        print(f"Error creating access card: {e}")
