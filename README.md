# Guest Access Card Generator

## Overview
This application processes guest data from a CSV file, generates personalized access cards with QR codes, and sends them via email.

## Setup

1. Install the required Python packages:
    ```bash
    pip install pandas qrcode[pil] pillow smtplib
    ```

2. Update the `config.py` file with your SMTP server details and other configuration settings.

3. Place your guest data CSV file in the `data/` directory.

4. Place your access card template image in the `templates/` directory.

5. Run the application:
    ```bash
    python src/main.py
    ```

## Files

- `data/guests.csv`: CSV file containing guest details.
- `templates/access_card_template.png`: Access card template image.
- `src/csv_processor.py`: Module for processing CSV files.
- `src/qr_code_generator.py`: Module for generating QR codes.
- `src/access_card_creator.py`: Module for creating access cards.
- `src/email_sender.py`: Module for sending emails.
- `src/main.py`: Main script to run the application.
- `config.py`: Configuration settings.
- `README.md`: Project documentation.
