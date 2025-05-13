import os
import sqlite3
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

def insert_to_db(spark, df):
    # Convert Spark DataFrame to Pandas for SQLite insertion
    pandas_df = df.toPandas()
    
    # Connect to SQLite database
    db_path = "/app/data/sparklab.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table dynamically based on DataFrame schema
    columns = pandas_df.columns
    # Assume all columns are TEXT for simplicity; adjust types if needed
    col_definitions = ", ".join([f"{col} TEXT" for col in columns])
    create_table_query = f"""
        CREATE TABLE IF NOT EXISTS people (
            {col_definitions}
        )
    """
    cursor.execute(create_table_query)
    
    # Drop existing data to avoid duplicates (use INSERT OR IGNORE for append)
    cursor.execute("DELETE FROM people")
    
    # Insert data
    placeholders = ", ".join(["?" for _ in columns])
    insert_query = f"INSERT INTO people ({', '.join(columns)}) VALUES ({placeholders})"
    for row in pandas_df.itertuples(index=False):
        cursor.execute(insert_query, tuple(row))
    
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