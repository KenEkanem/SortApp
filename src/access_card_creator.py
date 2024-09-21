from PIL import Image, ImageDraw, ImageFont
import os

def split_name(guest_name, max_words=3):
    words = guest_name.split()
    if len(words) > max_words:
        first_line = " ".join(words[:max_words])
        second_line = " ".join(words[max_words:])
        return first_line, second_line
    else:
        return guest_name, ""

def create_access_card(template_file, guest_name, guest_id, qr_code_file, color_name, output_file):
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
        second_line_position = (365, 1565)
        id_position = (363, 1670)

        # Split the guest name into two lines
        first_line, second_line = split_name(guest_name)

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

        # Define color mappings
        color_mapping = {
            "Red": (255, 0, 0),
            "Orange": (255, 165, 0),
            "Green": (0, 128, 0),
            "Blue": (51, 78, 172) 
        }

        # Get the color from the color name
        color_code = color_mapping.get(color_name, (0, 0, 0))  # Default to black if not found

        # Define the color code box area on the template
        color_box_top_left = (646, 1329)
        color_box_bottom_right = (866, 1392)

        # Draw a filled rectangle with the color
        print(f"Filling color: '{color_name}' ({color_code}) in box from {color_box_top_left} to {color_box_bottom_right}")
        draw.rectangle([color_box_top_left, color_box_bottom_right], fill=color_code)

        # Draw text on the image
        print(f"Drawing Name: '{first_line}' at {name_position}")
        draw.text(name_position, first_line, font=font, fill="black")
        
        if second_line:
            print(f"Drawing Second Line: '{second_line}' at {second_line_position}")
            draw.text(second_line_position, second_line, font=font, fill="black")
        
        print(f"Drawing ID: '{guest_id}' at {id_position}")
        draw.text(id_position, guest_id, font=font, fill="black")

        # Paste the QR code onto the template
        template.paste(qr_img, qr_position)

        # Save the final access card
        template.save(output_file)
        print(f"Access card created and saved as {output_file}")
        
    except Exception as e:
        print(f"Error creating access card: {e}")

