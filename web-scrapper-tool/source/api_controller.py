import flask
import time
import logging
from flask_cors import CORS
import search_helper as search
import main_scrapper as scrapper
from flask import request, jsonify, make_response

app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/api/search', methods=['GET'])
def api_search():
    if 'q' in request.args:
        highlighted = None
        try:
            phrase = search.get_phrase_fixer(str(request.args['q']))
            if len(phrase["suggest"]["phrase-fixer"][0]["options"]) > 0:
                text = phrase["suggest"]["phrase-fixer"][0]["options"][0]["text"]
                highlighted = phrase["suggest"]["phrase-fixer"][0]["options"][0]["highlighted"]
            else:
                text = phrase["suggest"]["phrase-fixer"][0]["text"]
            products = search.search(text)
            total = products["hits"]["total"]["value"]
            if total > 0:
                search.store_terms(text)
            response = []
            for p in products["hits"]["hits"]:
                response.append(p["_source"])
        except Exception as e:
            logging.exception("Exception")
            return make_response(jsonify(e), 500)
    else:
        return flask.Response(status=400)
    return make_response(jsonify({"fixedWord": highlighted, "total": total, "productsDetails": response}), 200)


@app.route('/api/get-predictive-term', methods=['GET'])
def api_predictive_term():
    if 'q' in request.args:
        try:
            terms = search.get_predictive_words(str(request.args['q']))
            response = []
            for term in terms["hits"]["hits"]:
                response.append(term["highlight"]["text"][0])
        except Exception as e:
            logging.exception("Exception")
            return make_response(jsonify(e), 500)
    else:
        return flask.Response(status=400)
    return make_response(jsonify(response), 200)


@app.route('/api/scrape', methods=['GET'])
def api_scrapping():
    if 'q' in request.args:
        try:
            scrapper.scrape(str(request.args['q']))
        except Exception as e:
            logging.exception("Exception")
            return make_response(jsonify(e), 500)
    else:
        return flask.Response(status=400)
    return make_response(True, 200)


if __name__ == '__main__':
    filename = time.strftime("%d-%m-%Y")
    logging.basicConfig(filename=filename + '.log', filemode='w',
                        format='%(name)s : %(levelname)s : %(asctime)s: %(message)s', datefmt='%H:%M:%S')
    app.run(host='localhost', port='5000')
