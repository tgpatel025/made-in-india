import logging
import json
from elasticsearch import Elasticsearch
from io import StringIO

file = open('elastic-search-models.json')
elasticsearch_data = json.load(file)


def connect_elasticsearch():
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    try:
        if es.ping():
            return es
    except Exception as es:
        return es


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
            print('Created Product Index')
    except Exception as ex:
        print(str(ex))


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
            print('Created Term Suggester Index')
    except Exception as ex:
        print(str(ex))


def create_phrase_fixer_index():
    index_name = "phrase-fixer"
    settings = {
        "settings": {
            "index": {
                "number_of_shards": 1,
                "number_of_replicas": 0,
                "max_ngram_diff": 50,
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
            print('Created Phrase Fixer Index')
    except Exception as ex:
        print(str(ex))


def store_record(record):
    try:
        if not es_object.exists(index='products', id=record['Product_ID']):
            es_object.index(index='products', body=record, id=record['Product_ID'])
        return
    except Exception as ex:
        return str(ex)


def store_phrase(record):
    try:
        phrase_fixer = {
            "text": record['Name']
        }
        if record['ID']:
            if not es_object.exists(index='keywords-suggester', id=record['ID']):
                return es_object.index(index='keywords-suggester', body=phrase_fixer, id=record['ID'])
        else:
            return es_object.index(index='keywords-suggester', body=phrase_fixer)
        return
    except Exception as ex:
        return str(ex)


def store_terms(record):
    try:
        keyword_suggester = {
            "text": record['Name'],
            "generic_name": record['Generic_Name'],
            "textKeyword": record['Name']
        }
        if record['ID']:
            if not es_object.exists(index='keywords-suggester', id=record['ID']):
                return es_object.index(index='keywords-suggester', body=keyword_suggester, id=record['ID'])
        else:
            return es_object.index(index='keywords-suggester', body=keyword_suggester)
    except Exception as ex:
        return str(ex)


def get_predictive_words(term):
    query = {
        "size": 5,
        "query": {
            "match": {
                "text": str(term)
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
                        "prune": True,
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
        return str(ex)


def search(term):
    query = {
        "query": {
            "match": {
                "Product_Name": {
                    "query": str(term)
                }
            }
        }
    }
    io = StringIO()
    try:
        return es_object.search(index='products', body=json.dumps(query))
    except Exception as ex:
        return str(ex)


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)

create_products_index()
create_keywords_suggester_index()
create_phrase_fixer_index()
# outcome = search('gas stove 3 burner')
# outcome = get_predictive_words('gas')
# print(json.dumps(outcome, sort_keys=True, indent=4))
