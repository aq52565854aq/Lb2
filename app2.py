from flask import Flask, request

app = Flask(__name__)


@app.route('/currency', methods=['GET'])
def get_currency():

    key = request.args.get('key')
    today = request.args.get('today')


    if today is not None and key is not None:
        return "USD - 41,5"
    else:
        return "Missing parameters", 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
