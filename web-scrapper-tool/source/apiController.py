import flask
from flask import request, jsonify, make_response
from source import searchHelper
import json
from flask_cors import CORS

app = flask.Flask(__name__)
app.config["DEBUG"] = True
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/api/search', methods=['GET'])
def api_search():
    if 'q' and 'gname' in request.args:
        try:
            phrase = searchHelper.get_phrase_fixer(str(request.args['q']))
            text = phrase["suggest"]["phrase-fixer"][0]["options"][0]["text"]
            highlighted = phrase["suggest"]["phrase-fixer"][0]["options"][0]["highlighted"]
            searchHelper.store_terms({'ID': None, 'Name': text, "Generic_Name": str(request.args['gname'])})
            products = searchHelper.search(text)
            response = []
            for product in products["hits"]["hits"]:
                response.append(product["_source"])
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
                obj = {"genericName": term["_source"]["generic_name"], "term": term["highlight"]["text"][0]}
                response.append(obj)
        except Exception as e:
            return make_response(jsonify(e), 500)
    else:
        return flask.Response(status=400)
    return make_response(jsonify(response), 200)


app.run()
