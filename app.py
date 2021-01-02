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

@app.route(config.endpoint, methods=['POST'])
def inbound_parse():
    """Process POST from Inbound Parse and print received data."""
    parse = Parse(config, request)
    # Sample processing action
    print("Email!")
    mail = mailparser.parse_from_string(parse.get_raw_email())
    print("Attachments", len(mail.attachments))
    for attached_file in mail.attachments:
        try:
            raw_payload = attached_file["payload"]
            payload_bytes = base64.b64decode(raw_payload)
            html_payload = payload_bytes.decode("utf-8")
            print(parse_highlights(html_payload))
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
