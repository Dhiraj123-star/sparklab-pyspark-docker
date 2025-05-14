from flask import Flask, jsonify, request
from main import create_spark_session, load_csv_data, insert_to_db
import sqlite3

app = Flask(__name__)
spark = create_spark_session()

@app.route("/", methods=["GET"])
def health_check():
    return {"status": "SparkLab Flask API is running"}

@app.route("/data", methods=["GET"])
def get_data():
    df = load_csv_data(spark)
    data = df.toPandas().to_dict(orient="records")
    return jsonify(data)

@app.route("/insert", methods=["POST"])
def insert_data():
    mode = request.args.get("mode", "overwrite")  # Default to overwrite
    if mode not in ["overwrite", "append"]:
        return jsonify({"status": "error", "message": "Invalid mode. Use 'overwrite' or 'append'."}), 400
    df = load_csv_data(spark)
    try:
        row_count = insert_to_db(spark, df, mode=mode)
        return jsonify({"status": "success", "rows_inserted": row_count, "mode": mode})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/db_data", methods=["GET"])
def get_db_data():
    try:
        # Connect to SQLite database
        db_path = "/app/data/sparklab.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Query all data from the people table
        cursor.execute("SELECT * FROM people")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        
        # Convert to list of dictionaries
        data = [dict(zip(columns, row)) for row in rows]
        
        # Close connection
        conn.close()
        
        return jsonify(data)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/data/<name>", methods=["GET"])
def get_data_by_name(name):
    try:
        db_path = "/app/data/sparklab.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM people WHERE name = ?", (name,))
        row = cursor.fetchone()
        columns = [desc[0] for desc in cursor.description]
        
        conn.close()
        
        if row:
            return jsonify(dict(zip(columns, row)))
        return jsonify({"status": "error", "message": f"No record found for name: {name}"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/data/<name>", methods=["PUT"])
def update_data(name):
    try:
        data = request.get_json()
        if not data or "age" not in data:
            return jsonify({"status": "error", "message": "Missing 'age' in request body"}), 400
        
        db_path = "/app/data/sparklab.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("UPDATE people SET age = ? WHERE name = ?", (data["age"], name))
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({"status": "error", "message": f"No record found for name: {name}"}), 404
        
        conn.commit()
        conn.close()
        
        return jsonify({"status": "success", "message": f"Updated record for name: {name}"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/data/<name>", methods=["DELETE"])
def delete_data(name):
    try:
        db_path = "/app/data/sparklab.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM people WHERE name = ?", (name,))
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({"status": "error", "message": f"No record found for name: {name}"}), 404
        
        conn.commit()
        conn.close()
        
        return jsonify({"status": "success", "message": f"Deleted record for name: {name}"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)