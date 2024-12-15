from flask import Flask, request
import requests

app = Flask(__name__)

BASE_URL = "https://api.kavenegar.com/v1/457059716562376C4D654B50486B6F4E58755A5A4538425A7233704E6F68417A5968564357764E477253733D/verify/lookup.json"

RECEPTORS = [
    "09353704931",
    "09120689914",
    "09101635006"
]

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    instance = data.get("commonLabels", {}).get("instance", "UNKNOWN")
    status = data.get("status", "UNKNOWN").upper()
    template = "monitor1"

    for receptor in RECEPTORS:
        params = {
            "receptor": receptor,
            "token": instance,
            "token2": status,
            "template": template
        }
        response = requests.get(BASE_URL, params=params)

        if response.status_code != 200:
            print(f"Failed to send SMS to {receptor}: {response.text}")
    
    return {"message": "Notifications sent successfully"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
