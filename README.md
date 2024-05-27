# create_enable_webhook
Create a Smartsheet webhook, verification process and can listens to webhook events.

Create Smartsheet Webhook Function:

create_smartsheet_webhook(api_token, sheet_id, callback_url):
Constructs the API endpoint URL for creating a webhook.
Sets the headers with the API token and content type as JSON.
Defines the payload with the webhook details.
Sends a POST request to the Smartsheet API to create the webhook.
Returns the response JSON if the request is successful, otherwise raises an error.
Webhook Endpoint:

@app.route('/webhook', methods=['POST']):
Checks for Smartsheet-Hook-Challenge in the request headers.
Responds with Smartsheet-Hook-Response in the response headers to complete the handshake.
Prints the received webhook event data.
Create Webhook Route:

@app.route('/create_webhook', methods=['POST']):
Calls the create_smartsheet_webhook function to create the webhook.
Returns the API response in JSON format or an error message.
Running the Application
Install Dependencies:

sh
Copy code
pip install -r requirements.txt
Run the Flask App:

sh
Copy code
python app.py
Create Webhook:

Send a POST request to http://localhost:5000/create_webhook to create the webhook.
Ensure you have a valid Smartsheet API token, sheet ID, and webhook callback URL configured in config.py.
