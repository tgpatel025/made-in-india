import flask
from flask import request, jsonify, make_response
# from .constants import *

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/api/search/', methods=['GET'])
def api_search():
    if 'q' in request.args:
        query = str(request.args['q'])
    else:
        return flask.Response(status=400)
    return make_response(jsonify({"query": query}), 200)


@app.route('/api/get-predictive-term', methods=['GET'])
def api_predictive_term():
    if 'q' in request.args:
        try:
            query = str(request.args['q'])
            # es_object = connect_elasticsearch()
            # res = search(es_object, 'products', query)
        except Exception as es:
            return make_response(jsonify(es), 500)
    else:
        return flask.Response(status=400)
    return make_response(jsonify('hello'), 200)


app.run()
