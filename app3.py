from flask import Flask, request, jsonify, make_response
app = Flask(__name__)
@app.route('/currency', methods=['GET'])
def get_currency():
    content_type = request.headers.get('Content-Type')
    data = {"currency": "USD", "rate": 41.5}
    if content_type == 'application/json':
        return jsonify(data)
    elif content_type == 'application/xml':
        xml_response = f'<response><currency>{data["currency"]}</currency><rate>{data["rate"]}</rate></response>'
        response = make_response(xml_response)
        response.headers['Content-Type'] = 'application/xml'
        return response
    else:
        return "USD - 41.5", 200, {'Content-Type': 'text/plain'}
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
