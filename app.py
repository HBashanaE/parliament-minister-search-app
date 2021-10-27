from flask import Flask, render_template, request, jsonify
from query_processing import es, build_query, classify_intent
import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')    

@app.route('/search', methods=['GET'])
def search():
    query  = request.args.get("query")
    intents, tokenized_query, query = classify_intent(query)
    body = build_query(query, tokenized_query, intents)
    print('Body: ', body)
    res = es.search(index="parliament", body=body)
    data = res['hits']['hits']
    # print(json.dumps(res, indent=4, ensure_ascii=False))
    return jsonify([i['_source'] for i in data])

if __name__ == '__main__':
    app.run(debug=True)
