from flask import request
from flask_api import FlaskAPI
from app.request_lookup import get_results, get_indexes

app = FlaskAPI(__name__)


@app.route('/', methods=['GET'])
def root():
    indexes = get_indexes()

    return dict(indexes=indexes)


@app.route('/<index>', methods=['GET'])
def search(index):
    query = request.args.get('q')
    if query:
        language = request.args.get('language', 'en')
        results = get_results(index, language, query)
        return dict(items=results, count=len(results))
    else:
        return "Enter /{}?q=Query".format(index)


@app.route('/status', methods=['GET'])
def status():
    return "OK"


@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response