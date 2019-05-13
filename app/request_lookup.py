import json
import os

import requests
from structlog import get_logger

from app import settings

logger = get_logger()
request_timeout = 30


def get_indexes():
    request_url = os.path.join(settings.LOOKUP_URL, '_cat/indices?format=json')

    try:
        resp = requests.get(request_url)
    except (requests.RequestException) as rte:
        logger.error(rte)
        raise Exception("ERROR IN LOOKUP API. TIMEOUT")

    if resp.status_code != 200:
        # This means something went wrong.
        logger.error('Request Failed', code=resp.status_code, reason=resp.reason)
        raise Exception("ERROR IN LOOKUP API.")

    results = json.loads(resp.text)

    return [result.get('index') for result in results]


def get_results(register, language, search_value):
    request_url = os.path.join(settings.LOOKUP_URL, register, '_search')

    request_json = get_request_json(language, search_value.lower())

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

    logger.info('Query Successful', took=results.get('took'))

    for result in results['hits']['hits']:
        result_value = {
            'en': {
                'text': result['_source'].get('en')
            }
        }

        if language != 'en':
            result_value[language] = {
                    'text': result['_source'].get(language)
                }

        if 'highlight' in result:
            if 'en' in result['highlight']:
                result_value['en']['highlight'] = result['highlight']['en'][0]

            if language != 'en' and language in result['highlight']:
                result_value[language]['highlight'] = result['highlight'][language][0]

        result_output.append(result_value)

    return result_output


def get_request_json(language, search_value):
    # Highest weighting for whole search_value
    should_terms = [
        {
            "term":
                {
                    "en":
                        {
                            "value": search_value,
                            "boost": 3.0
                        }
                }
        }
    ]

    if language != 'en':
        should_terms.append({
            "term":
                {
                    language:
                        {
                            "value": search_value,
                            "boost": 3.0
                        }
                }

        })

    # Then weight on each individual word
    split_search_values = search_value.split()
    if len(split_search_values) > 1:
        for word in split_search_values:
            should_terms.append({
                "term":
                    {
                        "en":
                            {
                                "value": word,
                                "boost": 2.0
                            }
                    }
            })

            if language != 'en':
                should_terms.append({
                    "term":
                        {
                            language:
                                {
                                    "value": word,
                                    "boost": 2.0
                                }
                        }
                })

    should_terms.append({
        "match": {
            "en.trigrams": search_value
        }
    })

    if language != 'en':
        should_terms.append({
            "match": {
                language + ".trigrams": search_value
            }
        })

    highlight = {
        "fields": {
            "en": {}
        }
    }

    if language != 'en':
        highlight["fields"][language] = {}

    return {
        "query": {
            "bool": {
                "should": should_terms,
                "minimum_should_match": 1,
                "boost": 1.0
            }
        },
        "highlight": highlight
    }
