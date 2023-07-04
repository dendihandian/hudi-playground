"""
docker-compose exec spark-hudi-master python src/custom_query_pyspark_read_mysql_table.py
"""

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("custom_query_pyspark_read_mysql_table") \
    .getOrCreate()

# Configure MySQL connection
jdbc_url = "jdbc:mysql://mysql:3306/test_db"
table_name = "test_table"
connection_properties = {
    "user": "root",
    "password": "example"
}

custom_query = f"SELECT * FROM {table_name} WHERE created_at > '2023-05-01 00:00:00'"

# Read data from MySQL table
df = spark.read \
    .format("jdbc") \
    .option("url", jdbc_url) \
    .option("query", custom_query) \
    .options(**connection_properties) \
    .load()

# Perform your desired data operations on the DataFrame
df.show()

# You can also perform additional transformations or aggregations on the DataFrame
# For example:
# df_filtered = df.filter(df['column'] > 10)
# df_grouped = df.groupby('column').agg({'other_column': 'sum'})

spark.stop()
