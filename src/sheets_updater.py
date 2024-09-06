import requests

# URL for Google Apps Script
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyIXQiGpZAFBrCd6_16jJlK5HIgtTiPBjzQwudNVomtH3_RvVtcbQ_tdNnjNJdkrdsYRQ/exec"

def update_barcode_in_sheet(email, unique_id, barcode_url):
    # Define the parameters for the POST request
    params = {
        'email': email,
        'unique_id': unique_id,
        'barcode': barcode_url,
        'action': 'generate_barcode'  
    }
    
    try:
        # Make the request to the Google Apps Script
        response = requests.post(GOOGLE_SCRIPT_URL, data=params)
        
        # Check the response from the Google Apps Script
        if response.status_code == 200:
            data = response.json()
            if 'error' in data:
                print(f"Failed to update barcode for {email}: {data['error']}")
            else:
                print(f"Barcode successfully updated for {email}")
                print(f"Response Data: {data}")
        else:
            print(f"Failed to update barcode for {email}: {response.status_code}")
            print(f"Response Text: {response.text}")
    except Exception as e:
        print(f"Error updating barcode: {str(e)}")
