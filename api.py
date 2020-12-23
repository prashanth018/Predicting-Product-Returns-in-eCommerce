import flask
from flask import request, jsonify
import predict as pd

app = flask.Flask(__name__)
app.config["DEBUG"] = True

predictResponse = {
    "skuId": {"score": "0.9", "reason": "Bad Product"},
    "skuId2": {"score": "0.9", "reason": ""},
    "skuI3": {"score": "0.9", "reason": "Fitting Issue"}
}


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"


@app.route('/api/v1/resources/predict', methods=['POST'])
def predict():
    print(request.json)
    response = pd.predict(request.json)
    # print(feature_extraction)
    name = ""
    if request.json["profileId"] == "se-1000":
        name = "Kim"
    elif request.json["profileId"] == "se-2000":
        name = "Mark"
    # print(list(response.keys())[0])
    print("Model predicted for the profile ", name, " (", request.json["profileId"], ") with Return Probability of ",
          response[list(response.keys())[0]]['score'])
    # print(name, "'s return probability: ", response[''])
    return jsonify(response), 201


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


app.run()
