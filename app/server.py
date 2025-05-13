from flask import Flask, jsonify
from main import create_spark_session, load_csv_data

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
