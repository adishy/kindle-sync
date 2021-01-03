"""Receiver module for processing SendGrid Inbound Parse messages.

See README.txt for usage instructions."""

try:
    from config import Config
except:
    # Python 3+, Travis
    from sendgrid.helpers.inbound.config import Config

try:
    from parse import Parse
except:
    # Python 3+, Travis
    from sendgrid.helpers.inbound.parse import Parse

from flask import Flask, request, render_template
from parse_highlights import parse_highlights
from sync_to_notion import SyncToNotion
import base64
import mailparser
import os

app = Flask(__name__)
config = Config()
data = "Not yet set"

@app.route('/', methods=['GET'])
def index():
    """Show index page to confirm that server is running."""
    return render_template('index.html')

@app.route('/last_email', methods=['GET'])
def last_email_saved():
    email_path = "last_email_saved.txt"
    if not os.path.exists(email_path):
        return "No emails were saved!"
    file = open(email_path, "r")
    return file.read()

@app.route(config.endpoint, methods=['POST'])
def inbound_parse():
    """Process POST from Inbound Parse and print received data."""
    parse = Parse(config, request)
    # Sample processing action
    print("Email!")
    raw_email = parse.get_raw_email()
    file = open("last_email_saved.txt", "w")
    file.write(raw_email)
    file.close()
    print("Saved last email")
    mail = mailparser.parse_from_string(raw_email)
    print("Attachments", len(mail.attachments))
    print("Attachments", mail.attachments)
    for attached_file in mail.attachments:
        try:
            raw_payload = attached_file["payload"]
            print(raw_payload)
            print(attached_file["content_transfer_encoding"])
            if attached_file["content_transfer_encoding"] == "base64":
                payload_bytes = base64.b64decode(raw_payload)
                html_payload = payload_bytes.decode("utf-8")
            else:
                html_payload = raw_payload
            highlights = parse_highlights(html_payload)
            print(f"Received and parsed highlights for {highlights['title']}")
            #SyncToNotion(highlights)
        except Exception as e:
            print(e)
            print("Could not process attached file")

    return "OK"

if __name__ == '__main__':
    # Be sure to set config.debug_mode to False in production
    port = int(os.environ.get("PORT", config.port))
    print(port)
    if port != config.port:
        config.debug = False
    app.run(host='0.0.0.0', debug=config.debug_mode, port=port)
