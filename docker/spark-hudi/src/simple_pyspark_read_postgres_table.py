"""
docker-compose exec spark-hudi-master python src/simple_pyspark_read_postgres_table.py
"""

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("PostgreSQL Query") \
    .getOrCreate()

# Configure PostgreSQL connection
jdbc_url = "jdbc:postgresql://postgres:5432/spark_hudi"
table_name = "test_table"
connection_properties = {
    "user": "admin",
    "password": "admin"
}

# Read data from PostgreSQL table
df = spark.read \
    .format("jdbc") \
    .option("url", jdbc_url) \
    .option("dbtable", table_name) \
    .option("driver", "org.postgresql.Driver") \
    .options(**connection_properties) \
    .load()

# Perform your desired data operations on the DataFrame
df.show()

# You can also perform additional transformations or aggregations on the DataFrame
# For example:
# df_filtered = df.filter(df['column'] > 10)
# df_grouped = df.groupby('column').agg({'other_column': 'sum'})

spark.stop()
