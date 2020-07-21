import flask
from flask import request, jsonify, make_response
from source import searchHelper
from flask_cors import CORS
import main_scrapper as ms

app = flask.Flask(__name__)
app.config["DEBUG"] = True
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/api/search', methods=['GET'])
def api_search():
    if 'q' in request.args:
        highlighted = None
        try:
            ms.search_query = str(request.args['q'])
            ms.get_product_link(ms.url)
            phrase = searchHelper.get_phrase_fixer(str(request.args['q']))
            if len(phrase["suggest"]["phrase-fixer"][0]["options"]) > 0:
                text = phrase["suggest"]["phrase-fixer"][0]["options"][0]["text"]
                highlighted = phrase["suggest"]["phrase-fixer"][0]["options"][0]["highlighted"]
            else:
                text = phrase["suggest"]["phrase-fixer"][0]["text"]
            searchHelper.store_terms(text)
            products = searchHelper.search(text)
            response = []
            for p in products["hits"]["hits"]:
                response.append(p["_source"])
        except Exception as e:
            return make_response(jsonify(e), 500)
    else:
        return flask.Response(status=400)
    return make_response(jsonify({"fixedWord": highlighted, "productsDetails": response}), 200)


@app.route('/api/get-predictive-term', methods=['GET'])
def api_predictive_term():
    if 'q' in request.args:
        try:
            terms = searchHelper.get_predictive_words(str(request.args['q']))
            response = []
            for term in terms["hits"]["hits"]:
                response.append(term["highlight"]["text"][0])
        except Exception as e:
            return make_response(jsonify(e), 500)
    else:
        return flask.Response(status=400)
    return make_response(jsonify(response), 200)


app.run()
