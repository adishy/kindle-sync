from kindle_sync import app

@app.route('/email/', methods = [ 'POST' ])
def test():
    print("Email!")

    for key, value in request.args.items():
        print(key, ":", value)

    return jsonify({ "status": 200 }) 