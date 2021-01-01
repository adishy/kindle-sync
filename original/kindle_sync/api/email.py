from kindle_sync import app
from flask import request, jsonify

@app.route('/api/email/', methods = [ 'POST' ])
def test():
    print("Email!")

    for key, value in request.args.items():
        print(key, ":", value)

    return jsonify({ "status": 200 }) 