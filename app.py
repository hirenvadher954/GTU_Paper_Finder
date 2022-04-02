__author__ = "Hiren Vadher"
__version__ = "1.0.1"
__email__ = "hirenvadher954@gmail.com"

from typing import Dict, Any, List

from flask import Flask
from datetime import date
import requests
from flask_cors import CORS
import json
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

paper: dict[str, str] = {}
list_of_urls: list[str] = []
year_list: range = range(2016, date.today().year)


@app.route('/<field>/<subject_code>')
def find_valid_paper(field: str, subject_code: str) -> json:
    for year in year_list:
        get_paper_link(field, subject_code, year, "S")
        get_paper_link(field, subject_code, year, "W")
    get_paper_status()
    array = [{'year': i, 'paperLink': paper[i]} for i in paper]
    return json.dumps(array)


def get_url(url: str):
    """
    It sends get request to a specified url.
    :param url: 
    :return requests.Response:
    """
    return requests.get(url)


def get_paper_status():
    """
    With the help of ThreadPoolExecutor, it sends a simultaneous get request to the generated URL so that we can
    verify the status code. The reason behind the use of ThreadPoolExecutor is that it speeds up the whole process of
    sending requests.
    """
    with ThreadPoolExecutor(max_workers=10) as pool:
        response_list = list(pool.map(get_url, list_of_urls))
    for index in range(len(response_list)):
        if response_list[index].status_code == 200:
            paper[str(year_list[index // 2]) + "-" + get_full_name(index)] = list_of_urls[index]


def get_paper_link(field, subject_code, year, summer_or_winter):
    """
    :param field:
    :param subject_code:
    :param year:
    :param summer_or_winter:

    It will return paper link E.g - https://www.gtu.ac.in/uploads/W2018/BE/3110013.pdf
    """
    paper_link = f"https://www.gtu.ac.in/uploads/{summer_or_winter}{year}/{field}/{subject_code}.pdf"
    list_of_urls.append(paper_link)
    # if requests.get(paper_link).status_code == 200:
    #     paper[str(year) + "-" + get_full_name(summer_or_winter)] = paper_link


def get_full_name(index):
    """
    Decide whether the paper is Summer or Winter
    :param index:
    :return :
    """
    if list_of_urls[index][30] == "S":
        return "Summer"
    return "Winter"


@app.after_request
def after_request_func(response):
    """
    After completion of every request, It clears global value.
    :param response:
    :return:
    """
    paper.clear()
    list_of_urls.clear()
    return response


if __name__ == '__main__':
    app.run()
