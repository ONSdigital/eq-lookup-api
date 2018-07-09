import json
import os
import requests
from app import settings
from structlog import get_logger

logger = get_logger()
request_timeout = 30

def get_results(register, data_type, search_value):
    request_url = os.path.join(settings.LOOKUP_URL, register, '_search')

    request_json = get_request_json(data_type, search_value.lower())

    try:
        resp = requests.post(request_url, json=request_json)
    except (requests.RequestException) as rte:
        logger.error(rte)
        raise Exception("ERROR IN LOOKUP API. TIMEOUT")

    if resp.status_code != 200:
        # This means something went wrong.
        logger.error('Request Failed', request_json=request_json, code=resp.status_code, reason=resp.reason)
        raise Exception("ERROR IN LOOKUP API.")

    result_output = []
    results = json.loads(resp.text)
    for result in results['hits']['hits']:
        occupation = result['highlight'][data_type][0] if 'highlight' in result else result['_source'][data_type]
        result_output.append(occupation)

    return result_output

def get_request_json(data_type, search_value):
    # Highest weighting for whole search_value
    should_terms = [
        {
            "term":
                {
                    data_type:
                        {
                            "value": search_value,
                            "boost": 3.0
                        }
                }
        }
    ]

    # Then weight on each individual word
    if len(search_value.split()) > 1:
        for word in search_value.split():
            should_terms.append({
                "term":
                {
                    data_type:
                        {
                            "value": word,
                            "boost": 2.0
                        }
                }
            })

    should_terms.append({
        "match": {
            data_type + ".trigrams": search_value
        }
    })

    return {
        "query": {
            "bool": {
                "should": should_terms,
                "minimum_should_match": 1,
                "boost": 1.0
            }
        },
        "highlight" : {
            "fields" : {
                data_type : {}
            }
        }
    }