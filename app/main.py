from pyspark.sql import SparkSession

def main():
    spark = SparkSession.builder \
        .appName("SparkLab") \
        .master("local[*]") \
        .getOrCreate()

    data = [("Alice", 25), ("Bob", 30), ("Cathy", 27)]
    df = spark.createDataFrame(data, ["Name", "Age"])
    df.show()

    spark.stop()

if __name__ == "__main__":
    main()
