# Guest Access Card Generator

A Python application that processes guest data from CSV files, generates personalized access cards with QR codes, and distributes them via email.

## Features

- CSV data processing for guest information
- QR code generation with embedded guest details
- Automated email distribution of access cards
- Error handling and logging
- Type hints for better code maintainability

## Prerequisites

- Python Python 3.11.2
- Virtual environment (recommended)

## Installation

1. Create and activate a virtual environment:

```bash
# For Linux/Mac
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

2. Install required packages:

```bash
pip install -r requirements.txt
```

## Configuration

### Create necessary directories:

- Create the data/ directory and place your guests.csv file inside.
- Create the qr_codes/ directory.
- Create `access_cards dir

### CSV File Format

Create a `guests.csv` file with the following columns:

```
name,email,unique_id,barcode,category,xn,checked_in,time_checked_in
```

### SMTP Configuration

Update the `.env` file with your SMTP server details, Google Client ID, and Google Client Secret configuration settings. see `env.example`

#### 

## Usage
1. Run the script:

```bash
cd src
python main.py
```

## Output

The script will:
1. Create an `access_cards` directory if it doesn't exist
2. Generate QR codes for each guest and save them in the directory
3. Send emails using SMTP to guests with their access cards attached

## QR Code Content

Each QR code contains:
- Guest name
- Email address
- Access level
- QR Code
- Event Date

## Error Handling

The application includes comprehensive error handling and logging:
- contributions needed

## Directory Structure

```
├── access_cards
│   └── Kennedy_Ekanem_access_card.png
├── config.py
├── data
│   └── guests.csv
├── qr_codes
│   ├── qr_PPAI1O7P2.png
│   └── qr_PPAIWE7P2.png
├── README.md
├── requirements.txt
├── src
│   ├── access_card_creator.py
│   ├── csv_processor.py
│   ├── email_content.py
│   ├── email_sender.py
│   ├── __init__.py
│   ├── main.py
│   ├── __pycache__
│   ├── qr_code_generator.py
│   ├── sheets_updater.py
│   └── token.pickle
├── templates
│   └── access_card_template.png
└── venv
    ├── bin
    ├── include
    ├── lib
    ├── lib64 -> lib
    ├── pyvenv.cfg
    └── share

```

## Contributing

To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
