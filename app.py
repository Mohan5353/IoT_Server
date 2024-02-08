# import pandas as pd
from flask import Flask, jsonify, request,render_template

app = Flask(__name__)
#
# html_code = b'''
# <html>
#     <body>
#         <h1>Hello Bro!</h1>
#     </body>
# </html>
# '''


@app.route('/')
def home():
    # global html_code
    return render_template("home.html"), 200


@app.route("/data", methods=["POST"])
def get_data():
    data = request.get_data()
    return render_template("received.html"), 201
