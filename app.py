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

from flask import Flask, request, render_template, make_response, jsonify
from parse_highlights import parse_highlights
from sync_to_notion import SyncToNotion
from pymongo import MongoClient
from bson.json_util import dumps, loads 
from os import environ as env
import base64
import mailparser
import os
import datetime

try:
    url = env["PI_TWO_MONGO_URL"]
    username = env["PI_TWO_MONGO_USER"]
    password = env["PI_TWO_MONGO_PASSWORD"]
    auth_source = "admin"
    mongo_uri = f"mongodb://{username}:{password}@{url}/?authSource={auth_source}"
    client = MongoClient(mongo_uri)
    db = client[env["PI_TWO_MONGO_DB_NAME"]]
    db_highlights_collection = db[env["PI_TWO_MONGO_HIGHLIGHTS_COLLECTION"]]
    db_emails_collection = db[env["PI_TWO_MONGO_EMAILS_COLLECTION"]]
except Exception as e:
    print(e)
    print("Could not instantiate PyMongo client")

app = Flask(__name__)
config = Config()

if not os.path.exists("tmp/"):
    os.mkdir("tmp")
    print("Created tmp directory!")

@app.route('/', methods=['GET'])
def index():
    """Show index page to confirm that server is running."""
    return render_template('index.html')

@app.route('/last_email', methods=['GET'])
def last_email_saved():
    number_of_emails = request.args.get("limit")
    if number_of_emails is None:
        number_of_emails = 1
    last_email = db_emails_collection.find({}).sort("created_timestamp").limit(int(number_of_emails))
    last_email = dumps(list(last_email))
    response = make_response(last_email, 200)
    response.mimetype = "application/json"
    return response

@app.route(config.endpoint, methods=['POST'])
def inbound_parse():
    """Process POST from Inbound Parse and print received data."""
    parse = Parse(config, request)
    print("Email!")
    raw_email = parse.get_raw_email()
    
    try:
        email = \
        {
            "raw_email": raw_email,
            "created_timestamp": datetime.datetime.now()
        }
        inserted_email = db_emails_collection.insert_one(email).inserted_id
        print("Saved last email in database!", inserted_email)
    except Exception as e:
        print(e)
        print("Could not save last email to database")
        
    mail = mailparser.parse_from_string(raw_email)
    print("Attachments", len(mail.attachments))
    for attached_file in mail.attachments:
        try:
            raw_payload = attached_file["payload"]
            if attached_file["content_transfer_encoding"] == "base64":
                payload_bytes = base64.b64decode(raw_payload)
                html_payload = payload_bytes.decode("utf-8")
            else:
                html_payload = raw_payload
            highlights = parse_highlights(html_payload)
            print(f"Received and parsed highlights for {highlights['title']}")

            try:
                inserted_highlights = db_highlights_collection.insert_one(highlights).inserted_id
                print("Saved highlights to database", inserted_highlights)
            except Exception as e:
                print(e)
                print("Could not save highlights to database")

            SyncToNotion(highlights)
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
