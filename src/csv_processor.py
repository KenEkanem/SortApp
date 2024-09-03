import pandas as pd

def load_guest_data(csv_file):
    try:
        # Load CSV and keep only the relevant columns
        guests = pd.read_csv(csv_file, usecols=['name', 'email', 'unique_id', 'xn', 'barcode'])
        return guests
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return None
