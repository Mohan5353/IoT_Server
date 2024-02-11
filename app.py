import pandas as pd
import uuid
from datetime import datetime
from github import Github
from flask import Flask, request, render_template

git = Github("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")
repo = git.get_user().get_repo("IoT_Server")
previous_sha = ""
previous_path = ""

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
    global sensor_data, previous_sha, previous_path
    df = pd.DataFrame(sensor_data)
    if previous_sha:
        repo.delete_file(path=previous_path, message="Deleted", sha=previous_sha)
    previous_path = f"{uuid.uuid1()}.csv"
    commit = repo.create_file(path=previous_path, message=f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                              content=df.to_csv(), branch="main")
    previous_sha = commit['commit'].sha
    return render_template("save.html"), 202


if __name__ == '__main__':
    app.run(debug=True, port=80, host="0.0.0.0")
