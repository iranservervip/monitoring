from flask import Flask, request
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Get Payamak Panel credentials and settings from environment variables
USERNAME = os.getenv('PAYAMAK_USERNAME')
PASSWORD = os.getenv('PAYAMAK_PASSWORD')
FROM = os.getenv('PAYAMAK_FROM')
TO = os.getenv('PAYAMAK_TO')

# Payamak Panel API endpoint
SMS_API_URL = 'https://api.payamak-panel.com/post/sendsms.ashx'

@app.route('/send-sms', methods=['POST'])
def send_sms():
    # Get the alert data from Alertmanager
    alert_data = request.json
    alert_name = alert_data.get('commonLabels', {}).get('alertname', 'No Alert Name')
    severity = alert_data.get('commonLabels', {}).get('severity', 'No Severity')
    summary = alert_data.get('annotations', {}).get('summary', 'No Summary')

    # Construct the SMS message
    message = f"Alert: {alert_name}\nSeverity: {severity}\nSummary: {summary}"

    # Send the SMS via Payamak Panel API
    payload = {
        'username': USERNAME,
        'password': PASSWORD,
        'to': TO,
        'from': FROM,
        'text': message
    }

    # Make the API request to Payamak Panel
    response = requests.get(SMS_API_URL, params=payload)

    # Check if the SMS was successfully sent
    if response.status_code == 200:
        return 'SMS sent successfully', 200
    else:
        return 'Failed to send SMS', 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

