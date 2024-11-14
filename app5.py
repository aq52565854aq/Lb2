from flask import Flask, jsonify, request, abort
from pydantic import BaseModel, ValidationError
import sqlite3
import os
app = Flask(__name__)
class DataModel(BaseModel):
    text: str
def init_db():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()
init_db()
@app.route("/save-data", methods=["POST"])
def save_data():
    try:
        data = DataModel(**request.get_json())
    except ValidationError as e:
        abort(400, description=str(e))
    with open("data.txt", "a", encoding="utf-8") as file:
        file.write(data.text + "\n")
    try:
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO data (text) VALUES (?)", (data.text,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        abort(500, description="Database error")
    finally:
        conn.close()
    return jsonify({"message": "Data saved successfully"})
if __name__ == "__main__":
    app.run(debug=True)


