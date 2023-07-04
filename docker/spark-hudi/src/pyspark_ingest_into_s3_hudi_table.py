"""
docker-compose exec spark-hudi-master python src/pyspark_ingest_into_s3_hudi_table.py
"""

from pyspark.sql import SparkSession
from os import getenv

S3_BUCKET = getenv('S3_BUCKET')

spark = SparkSession.builder \
    .appName("pyspark_ingest_into_s3_hudi_table") \
    .config('spark.serializer', 'org.apache.spark.serializer.KryoSerializer') \
    .config('spark.sql.catalog.spark_catalog','org.apache.spark.sql.hudi.catalog.HoodieCatalog') \
    .config('spark.sql.extensions', 'org.apache.spark.sql.hudi.HoodieSparkSessionExtension') \
    .getOrCreate()

# Configure MySQL connection
database_name           = "test_db"
jdbc_url                = "jdbc:mysql://mysql:3306/test_db"
table_name              = "test_table"
connection_properties   = {"user": "root", "password": "example"}

custom_query = f"SELECT * FROM {table_name} WHERE created_at > '2023-05-01 00:00:00'"

# Read data from MySQL table
df = spark.read \
    .format("jdbc") \
    .option("url", jdbc_url) \
    .option("query", custom_query) \
    .options(**connection_properties) \
    .load()

try:
    hudi_options = {
        'hoodie.table.name': table_name,
        'hoodie.datasource.write.recordkey.field': 'id',
        'hoodie.datasource.write.partitionpath.field': 'created_at',
        'hoodie.datasource.write.table.name': table_name,
        'hoodie.datasource.write.operation': 'upsert',
        'hoodie.datasource.write.precombine.field': 'id',
        'hoodie.upsert.shuffle.parallelism': 2,
        'hoodie.insert.shuffle.parallelism': 2
    }

    df.write.format("hudi"). \
        options(**hudi_options). \
        mode("overwrite"). \
        save(f"s3a://{S3_BUCKET}/hudi_test/test_db/{table_name}/")

except Exception as e:
    print(e)

spark.stop()
