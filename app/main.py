import os
from pyspark.sql import SparkSession

def create_spark_session():
    return SparkSession.builder \
        .appName("SparkLab") \
        .master("local[*]") \
        .getOrCreate()

def load_csv_data(spark):
    # Use absolute path inside the container
    csv_path = "/app/data/people.csv"
    return spark.read.csv(csv_path, header=True, inferSchema=True)

def main():
    spark = create_spark_session()
    df = load_csv_data(spark)
    df.show()
    spark.stop()

if __name__ == "__main__":
    main()
