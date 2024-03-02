from warnings import filterwarnings

filterwarnings('ignore')

import pandas as pd
import uuid
from datetime import datetime
from github import Github
from flask import Flask, request, render_template

tkn = "ghp_woRfkw4J7exenb" + "vsqoHhN7i" + "EpbASbJ4cJAi8"
git = Github(tkn)
repo = git.get_user().get_repo("IoT_Server")

app = Flask(__name__)

sensor_data = pd.DataFrame(data={'Temperature': [], 'Humidity': [], 'Soil Moisture': [], 'PH': [], 'Rain Level': []},
                           dtype='float32')


@app.route('/')
def home():
    return render_template("home.html"), 200


@app.route("/data", methods=["POST"])
def get_data():
    sensor_data = pd.read_csv("data.csv")
    data = pd.DataFrame(eval(request.get_data()))
    print(data)
    pd.concat([data, sensor_data]).to_csv("data.csv")
    return render_template("received.html"), 201


@app.route('/save', methods=["GET"])
def save_data():
    data = pd.read_csv("data.csv")
    for col in data.columns:
      if col not in ['Temperature', 'Humidity', 'Soil Moisture', 'PH', 'Rain Level']:
          data.drop([col], axis=1, inplace=True)
    repo.create_file(path=f"data/{uuid.uuid1()}.csv", message=f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                     content=data.to_csv(), branch="main")
    print(data)
    return render_template("save.html"), 202


if __name__ == '__main__':
    app.run(debug=True, port=80, host="0.0.0.0")
