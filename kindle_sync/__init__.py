from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from kindle_sync.api import *
from kindle_sync.views import *