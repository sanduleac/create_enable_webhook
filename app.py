import requests
from flask import Flask, request, jsonify
import config

app = Flask(__name__)

def create_smartsheet_webhook(api_token, sheet_id, callback_url):
    url = "https://api.smartsheet.com/2.0/webhooks"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "name": "My Webhook",
        "callbackUrl": callback_url,
        "scope": "sheet",
        "scopeObjectId": sheet_id,
        "events": ["*.*"],
        "version": 1
    }

    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def enable_smartsheet_webhook(api_token, webhook_id):
    url = f"https://api.smartsheet.com/2.0/webhooks/{webhook_id}"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "enabled": True
    }

    response = requests.put(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

@app.route('/webhook', methods=['POST'])
def webhook():
    if 'Smartsheet-Hook-Challenge' in request.headers:
        challenge = request.headers['Smartsheet-Hook-Challenge']
        return jsonify({'smartsheetHookResponse': challenge}), 200, {'Smartsheet-Hook-Response': challenge}
    
    event_data = request.json
    print("Webhook event received:", event_data)
    
    return '', 200

@app.route('/create_and_enable_webhook', methods=['POST'])
def create_and_enable_webhook():
    try:
        # Step 1: Create the webhook
        webhook_response = create_smartsheet_webhook(config.SMARTSHEET_API_TOKEN, config.SHEET_ID, config.WEBHOOK_CALLBACK_URL)
        webhook_id = webhook_response['id']
        
        # Step 2: Enable the webhook and wait for the verification process
        enable_response = enable_smartsheet_webhook(config.SMARTSHEET_API_TOKEN, webhook_id)
        
        return jsonify(enable_response)
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(port=5000)
