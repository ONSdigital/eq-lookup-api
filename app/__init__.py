from flask import request
from flask_api import FlaskAPI
from app.request_lookup import get_results

app = FlaskAPI(__name__)


@app.route('/', methods=['GET'])
def root():
    return "</br>/country/ or </br>/industry/ or </br>/occupation/ or </br>"


@app.route('/status', methods=['GET'])
def status():
    return "OK"


@app.route('/country/', methods=['GET'])
def country_search():
    query = request.args.get('q')
    if query:
        countries = get_results('countries', 'country', query)
        return dict(countries=countries, count=len(countries))
    else:
        return "Enter country/?q=Country"


@app.route('/occupation/', methods=['GET'])
def occupation_search():
    query = request.args.get('q')
    if query:
        occupations = get_results('occupations', 'occupation', query)
        return dict(occupations=occupations, count=len(occupations))
    else:
        return "Enter occupation/?q=Occupation"


@app.route('/industry/', methods=['GET'])
def industry_search():
    query = request.args.get('q')
    if query:
        industries = get_results('industries', 'industry', query)
        return dict(industries=industries, count=len(industries))
    else:
        return "Enter industry/?q=Industry"


@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response