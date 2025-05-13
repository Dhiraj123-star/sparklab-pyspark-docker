from flask import Flask, jsonify
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
    df = load_csv_data(spark)
    try:
        row_count = insert_to_db(spark, df)
        return jsonify({"status": "success", "rows_inserted": row_count})
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)