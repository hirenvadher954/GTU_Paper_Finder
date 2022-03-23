__author__ = "Hiren Vadher"
__version__ = "1.0.1"
__email__ = "hirenvadher954@gmail.com"

from flask import Flask
from datetime import date
import requests
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

paper = {}


@app.route('/<field>/<subject_code>')
def find_valid_paper(field, subject_code):
    for year in range(2016, date.today().year):
        get_paper(field, subject_code, year, "S")
        get_paper(field, subject_code, year, "W")
    array = [{'year': i, 'paperLink': paper[i]} for i in paper]
    return json.dumps(array)


def get_full_name(summer_or_winter):
    if summer_or_winter == "S":
        return "Summer"
    return "Winter"


def get_paper(field, subject_code, year, summer_or_winter):
    paper_link = f"https://www.gtu.ac.in/uploads/{summer_or_winter}{year}/{field}/{subject_code}.pdf"
    if requests.get(paper_link).status_code == 200:
        paper[str(year) + "-" + get_full_name(summer_or_winter)] = paper_link


@app.after_request
def after_request_func(response):
    paper.clear()
    return response


if __name__ == '__main__':
    app.run()
