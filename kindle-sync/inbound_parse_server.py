from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/test', methods = [ 'POST' ])
def test():
    body = request.get_json()
    print("Request:", body)
    return jsonify({ "status": 200 }) 

@app.route('/')
def index():
  return "<h1>Hello there!</h1>"

if __name__ == '__main__':
    app.run(port = 8000, host = '0.0.0.0', debug = True)