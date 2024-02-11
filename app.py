import pandas as pd
import uuid
from datetime import datetime
from github import Github
from flask import Flask, request, render_template

git = Github("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")
repo = git.get_user().get_repo("IoT_Server")

app = Flask(__name__)

sensor_data = {'Temperature': [], 'Humidity': [], 'Soil Moisture': [], 'PH': [], 'Rain Level': []}


@app.route('/')
def home():
    return render_template("home.html"), 200


@app.route("/data", methods=["POST"])
def get_data():
    global sensor_data
    data = eval(request.get_data())
    for item in sensor_data.keys():
        sensor_data[item].append(data[item])
    return render_template("received.html"), 201


@app.route('/save', methods=["GET"])
def save_data():
    global sensor_data
    df = pd.DataFrame(sensor_data)
    repo.create_file(path=f"data/{uuid.uuid1()}.csv", message=f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                     content=df.to_csv(), branch="main")
    return render_template("save.html"), 202


if __name__ == '__main__':
    app.run(debug=True, port=80, host="0.0.0.0")
