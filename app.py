import pandas as pd
import uuid
from datetime import datetime
from github import Github
from flask import Flask, request, render_template

tkn = "ghp_woRfkw4J7exenb" + "vsqoHhN7i" + "EpbASbJ4cJAi8"
git = Github(tkn)
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
    print(sensor_data)
    return render_template("received.html"), 201


@app.route('/save', methods=["GET"])
def save_data():
    global sensor_data
    df = pd.DataFrame(sensor_data)
    print(df)
    repo.create_file(path=f"data/{uuid.uuid1()}.csv", message=f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                     content=df.to_csv(), branch="main")
    return render_template("save.html"), 202

