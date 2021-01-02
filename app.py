"""Receiver module for processing SendGrid Inbound Parse messages.

See README.txt for usage instructions."""
import base64

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
import os

app = Flask(__name__)
config = Config()


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
    data = parse.get_raw_email()
    try:
        print(data)
        file = open('test.txt', 'w')
        file.write(data)
        file.close()
    except Exception as e:
        print("Could not write file")

    return "OK"

if __name__ == '__main__':
    # Be sure to set config.debug_mode to False in production
    port = int(os.environ.get("PORT", config.port))
    print(port)
    if port != config.port:
        config.debug = False
    app.run(host='0.0.0.0', debug=config.debug_mode, port=port)
