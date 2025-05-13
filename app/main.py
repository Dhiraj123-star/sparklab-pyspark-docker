import os
from pyspark.sql import SparkSession

def main():
    spark = SparkSession.builder \
        .appName("SparkLab") \
        .master("local[*]") \
        .getOrCreate()

    # Use absolute path inside the container
    csv_path = "/app/data/people.csv"
    df = spark.read.csv(csv_path, header=True, inferSchema=True)
    df.show()

    spark.stop()

if __name__ == "__main__":
    main()