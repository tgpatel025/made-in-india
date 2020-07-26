import json
import hashlib
import logging
from elasticsearch import Elasticsearch

file = open('../extra/elastic-search-models.json')
elasticsearch_data = json.load(file)


def connect_elasticsearch():
    es = Elasticsearch([{'host': 'made-in-india.search', 'port': 80}])
    try:
        if es.ping():
            return es
    except Exception as ex:
        logging.exception("Exception")
        return ex


es_object = connect_elasticsearch()


def create_products_index():
    index_name = "products"
    settings = {
        "settings": {
            "index": {
                "number_of_shards": 3,
                "number_of_replicas": 1
            }
        },
        "aliases": {},
        "mappings": elasticsearch_data["products"]
    }
    try:
        if not es_object.indices.exists(index_name):
            es_object.indices.create(index=index_name, body=settings)
            logging.info('Created Product Index')
    except Exception as ex:
        logging.exception("Elasticsearch is not started Exception")
        return str(ex)


def create_keywords_suggester_index():
    index_name = "keywords-suggester"
    settings = {
        "settings": {
            "index": {
                "number_of_shards": 1,
                "number_of_replicas": 0,
                "max_ngram_diff": 50,
                "analysis": {
                    "analyzer": {
                        "nGram_analyzer": elasticsearch_data["nGram_analyzer"],
                        "whitespace_analyzer": elasticsearch_data["whitespace_analyzer"]
                    },
                    "tokenizer": {
                        "nGram_filter": elasticsearch_data["nGram_filter"]
                    }
                }
            }
        },
        "aliases": {},
        "mappings": elasticsearch_data["keyword-suggester"]
    }
    try:
        if not es_object.indices.exists(index_name):
            es_object.indices.create(index=index_name, body=settings)
            logging.info('Created Term Suggester Index')
    except Exception as ex:
        logging.exception("Elasticsearch is not started Exception")
        return str(ex)


def create_phrase_fixer_index():
    index_name = "phrase-fixer"
    settings = {
        "settings": {
            "index": {
                "number_of_shards": 1,
                "number_of_replicas": 0,
                "analysis": {
                    "filter": {
                        "shingle": elasticsearch_data["shingle"]
                    },
                    "analyzer": {
                        "trigram": elasticsearch_data["trigram"]
                    }
                }
            }
        },
        "aliases": {},
        "mappings": elasticsearch_data["phrase-fixer"]
    }
    try:
        if not es_object.indices.exists(index_name):
            es_object.indices.create(index=index_name, body=settings)
            logging.info('Created Phrase Fixer Index')
    except Exception as ex:
        logging.exception("Elasticsearch is not started Exception")
        return str(ex)


def store_record(record):
    try:
        es_object.index(index='products', body=record, id=record['Product_ID'])
        logging.info('product stored successfully')
    except Exception as ex:
        logging.exception("Exception")
        return str(ex)


def store_phrase(text):
    try:
        phrase_fixer = {
            "text": text
        }
        hash_id = hashlib.sha1(text.encode())
        es_object.index(index='phrase-fixer', body=phrase_fixer, id=hash_id.hexdigest())
        logging.info('phrase stored successfully')
    except Exception as ex:
        logging.exception("Exception")
        return str(ex)


def store_terms(text):
    try:
        keyword_suggester = {
            "text": text,
            "textKeyword": text
        }
        hash_id = hashlib.sha1(text.encode())
        es_object.index(index='keywords-suggester', body=keyword_suggester, id=hash_id.hexdigest())
        logging.info('term stored successfully')
    except Exception as ex:
        logging.exception("Exception")
        return str(ex)


def get_predictive_words(term):
    query = {
        "size": 5,
        "query": {
            "multi_match": {
                "query": str(term),
                "fields": [
                    "text",
                    "textKeyword"
                ]
            }
        },
        "sort": [
            "_score"
        ],
        "highlight": {
            "fields": {
                "text": {}
            },
            "pre_tags": [
                "<b>"
            ],
            "post_tags": [
                "</b>"
            ]
        }
    }
    try:
        return es_object.search(index='keywords-suggester', body=json.dumps(query))
    except Exception as ex:
        logging.exception("Exception")
        return str(ex)


def get_phrase_fixer(text):
    query = {
        "suggest": {
            "phrase-fixer": {
                "text": text,
                "phrase": {
                    "field": "text.trigram",
                    "confidence": 0,
                    "collate": {
                        "query": {
                            "source": {
                                "match_phrase": {
                                    "title": "{{suggestion}}"
                                }
                            }
                        },
                        "prune": True
                    },
                    "highlight": {
                        "pre_tag": "<b>",
                        "post_tag": "</b>"
                    }
                }
            }
        }
    }
    try:
        return es_object.search(index='phrase-fixer', body=query)
    except Exception as ex:
        logging.exception("Exception")
        return str(ex)


def search(term):
    query = {
        "size": 100,
        "query": {
            "multi_match": {
                "query": str(term),
                "fields": [
                    "Product_Name",
                    "Product_Generic_Name"
                ],
                "fuzziness": "auto"
            }
        }
    }
    try:
        return es_object.search(index='products', body=json.dumps(query))
    except Exception as ex:
        logging.exception("Exception")
        return str(ex)


if __name__ == '__main__':
    logging.basicConfig(filename='logs', filemode='w', format='%(name)s : %(levelname)s : %(asctime)s: %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S')

create_products_index()
create_keywords_suggester_index()
create_phrase_fixer_index()
