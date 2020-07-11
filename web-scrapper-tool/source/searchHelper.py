import logging
import json
from .models import *
from elasticsearch import Elasticsearch


def connect_elasticsearch():
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if es.ping():
        print('Connected Successfully')
    else:
        print('Aww could not connect')
    return es


def create_products_index(es_object, index_name='products'):
    settings = {
        "settings": {
            "number_of_shards": 3,
            "number_of_replicas": 1
        },
        "mappings": {
            "dynamic": "strict",
            "properties": {
                "productGuid": {
                    "type": "text"
                },
                "dataId": {
                    "type": "text"
                },
                "fullName": {
                    "type": "text"
                },
                "price": {
                    "type": "text"
                },
                "origin": {
                    "type": "text"
                }
            }
        }
    }
    try:
        if not es_object.indices.exists(index_name):
            es_object.indices.create(index=index_name, body=settings)
            print('Created Product Index')
    except Exception as ex:
        print(str(ex))


def create_product_metadata_index(es_object, index_name='product_metadata'):
    settings = {
        "settings": {
            "number_of_shards": 3,
            "number_of_replicas": 1
        },
        "mappings": {
            "dynamic": "strict",
            "properties": {
                "productGuid": {
                    "type": "text"
                },
                "productData1": {
                    "type": "text"
                },
                "productData2": {
                    "type": "text"
                },
                "productData3": {
                    "type": "text"
                },
                "productData4": {
                    "type": "text"
                },
                "productData5": {
                    "type": "text"
                },
                "productData6": {
                    "type": "text"
                },
                "productData7": {
                    "type": "text"
                },
                "productData8": {
                    "type": "text"
                },
                "productData9": {
                    "type": "text"
                },
                "productData10": {
                    "type": "text"
                }
            }
        }
    }
    try:
        if not es_object.indices.exists(index_name):
            es_object.indices.create(index=index_name, body=settings)
            print('Created Product Metadata Index')
    except Exception as ex:
        print(str(ex))


def suggester(es_object, term, index_name='products'):
    suggest = {
        "suggest": {
            "term-suggest": {
                "prefix": term,
                "completion": {
                    "field": "fullName",
                    "size": 5
                },
                "fuzzy": {
                    "fuzziness": 1
                }
            }
        }
    }
    try:
        return es_object.suggest(index=index_name, body=suggest)
    except Exception as ex:
        return str(ex)


def store_record(es_object, index_name, record):
    try:
        return es_object.index(index=index_name, doc_type='salads', body=record)
    except Exception as ex:
        return ex


def search(es_object, index_name, query_term):
    query = {
        "query": {
            "match": {
                "fullName": query_term
            }
        }
    }
    try:
        return es_object.search(index=index_name, body=json.dump(query))
    except Exception as ex:
        return ex


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)

