"""
docker-compose exec spark-hudi-master python src/simple_pyspark_read_mysql_table.py
"""

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("MySQL Query") \
    .getOrCreate()

# Configure MySQL connection
jdbc_url = "jdbc:mysql://mysql:3306/spark_hudi"
table_name = "test_table"
connection_properties = {
    "user": "root",
    "password": "example"
}

# Read data from PostgreSQL table
df = spark.read \
    .format("jdbc") \
    .option("url", jdbc_url) \
    .option("dbtable", table_name) \
    .options(**connection_properties) \
    .load()

# Perform your desired data operations on the DataFrame
df.show()

# You can also perform additional transformations or aggregations on the DataFrame
# For example:
# df_filtered = df.filter(df['column'] > 10)
# df_grouped = df.groupby('column').agg({'other_column': 'sum'})

spark.stop()