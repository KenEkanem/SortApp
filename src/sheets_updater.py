import requests

# URL for Google Apps Script
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwpYPdv8pf_4nLaAg7bP1IqHsTIETdJwBF8hRVy2micuD9EyKm9m0chcODUofWFGtDWJA/exec"

def update_barcode_in_sheet(email, user_id):
    # Define the parameters for the POST request
    params = {
        'email': email,
        'unique_id': user_id
    }
    
    try:
        # Make the request to the Google Apps Script
        response = requests.post(GOOGLE_SCRIPT_URL, data=params)
        
        if response.status_code == 200:
            data = response.json()
            print(f"Barcode successfully updated for {email}")
            print(f"Response Data: {data}")
        else:
            print(f"Failed to update barcode for {email}: {response.status_code}")
            print(f"Response Text: {response.text}")
    except Exception as e:
        print(f"Error updating barcode: {str(e)}")

