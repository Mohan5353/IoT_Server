# import pandas as pd
from flask import Flask, jsonify, request

app = Flask(__name__)

html_code = b'''
<html>
    <body>
        <h1>Hello Bro!</h1>
    </body>
</html>
'''


@app.route('/')
def home():
    global html_code
    return html_code, 200


@app.route("/data", methods=["POST"])
def get_data():
    data = request.get_data()
    print(data)
    return html_code, 201


if __name__ == '__main__':
    app.run(debug=False, port=80, host="0.0.0.0")
