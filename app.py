__author__ = "Hiren Vadher"
__version__ = "1.0.1"
__email__ = "hirenvadher954@gmail.com"

from flask import Flask, jsonify, render_template
from datetime import date
import requests

app = Flask(__name__)

paper = {}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/BE')
def result():
    return render_template('result.html')


@app.route('/<field>/<subject_code>')
def find_valid_paper(field, subject_code):
    for year in range(2016, date.today().year):
        get_paper(field, subject_code, year, "S")
        get_paper(field, subject_code, year, "W")
    return jsonify(paper)


def get_paper(field, subject_code, year, summer_or_winter):
    paper_link = f"https://www.gtu.ac.in/uploads/{summer_or_winter}{year}/{field}/{subject_code}.pdf"
    if requests.get(paper_link).status_code == 200:
        paper[str(year) + summer_or_winter] = paper_link


@app.after_request
def after_request_func(response):
    paper.clear()
    return response


if __name__ == '__main__':
    app.run()
