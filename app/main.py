import os
import sqlite3
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

def create_spark_session():
    return SparkSession.builder \
        .appName("SparkLab") \
        .master("local[*]") \
        .getOrCreate()

def load_csv_data(spark):
    # Use absolute path inside the container
    csv_path = "/app/data/people.csv"
    # Define schema for validation
    schema = StructType([
        StructField("name", StringType(), False),  # Non-nullable string
        StructField("age", IntegerType(), True)   # Nullable integer
    ])
    df = spark.read.csv(csv_path, header=True, schema=schema)
    return df

def insert_to_db(spark, df, mode="overwrite"):
    # Convert Spark DataFrame to Pandas for SQLite insertion
    pandas_df = df.toPandas()
    
    # Connect to SQLite database
    db_path = "/app/data/sparklab.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table with specific types
    create_table_query = """
        CREATE TABLE IF NOT EXISTS people (
            name TEXT NOT NULL,
            age INTEGER,
            PRIMARY KEY (name)
        )
    """
    cursor.execute(create_table_query)
    
    # Clear table only in overwrite mode
    if mode == "overwrite":
        cursor.execute("DELETE FROM people")
    
    # Insert data
    insert_query = "INSERT OR IGNORE INTO people (name, age) VALUES (?, ?)"
    for row in pandas_df.itertuples(index=False):
        cursor.execute(insert_query, (row.name, row.age))
    
    # Commit and close
    conn.commit()
    conn.close()
    
    return len(pandas_df)

def main():
    spark = create_spark_session()
    df = load_csv_data(spark)
    df.show()
    spark.stop()

if __name__ == "__main__":
    main()