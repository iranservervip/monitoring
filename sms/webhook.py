from flask import Flask, request
import requests

app = Flask(__name__)

BASE_URL = "https://api.kavenegar.com/v1/457059716562376C4D654B50486B6F4E58755A5A4538425A7233704E6F68417A5968564357764E477253733D/verify/lookup.json"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    instance = data.get("commonLabels", {}).get("instance", "UNKNOWN")
    status = data.get("status", "UNKNOWN").upper()

    receptor = "09354389143"
    template = "monitor1"
    params = {
        "receptor": receptor,
        "token": instance,
        "token2": status,
        "template": template
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        return {"message": "Notification sent successfully"}, 200
    else:
        return {"error": "Failed to send notification", "details": response.text}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
