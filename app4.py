from flask import Flask, jsonify, request, abort
from datetime import datetime, timedelta
import requests

app = Flask(__name__)

def get_usd_rate(date: str):
    url = f"https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=USD&date={date}&json"
    response = requests.get(url)
    if response.status_code == 200 and response.json():
        return response.json()[0]['rate']
    else:
        return None

@app.route("/currency", methods=["GET"])
def get_currency():
    param = request.args.get("param")
    today = datetime.now().strftime("%Y%m%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")

    if param == "today":
        rate = get_usd_rate(today)
    elif param == "yesterday":
        rate = get_usd_rate(yesterday)
    else:
        abort(400, description="Invalid param value. Use 'today' or 'yesterday'.")

    if rate is None:
        abort(404, description="Exchange rate not found.")

    return jsonify({"date": today if param == "today" else yesterday, "rate": rate})

if __name__ == "__main__":
    app.run(debug=True)

