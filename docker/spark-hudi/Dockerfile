FROM bitnami/spark:3.3

# copy source
COPY src /opt/bitnami/spark/pyspark/src

# use root user to install required tools
USER root

# install required tools
RUN apt-get update
RUN apt-get install -y curl

# additional jars for Spark and Apache Hudi
RUN curl https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.1/hadoop-aws-3.3.1.jar --output /opt/bitnami/spark/jars/hadoop-aws-3.3.1.jar
RUN curl https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.11.1034/aws-java-sdk-bundle-1.11.1034.jar --output /opt/bitnami/spark/jars/aws-java-sdk-bundle-1.11.1034.jar
RUN curl https://repo1.maven.org/maven2/mysql/mysql-connector-java/5.1.49/mysql-connector-java-5.1.49.jar --output /opt/bitnami/spark/jars/mysql-connector-java-5.1.49.jar
RUN curl https://repo1.maven.org/maven2/org/apache/hudi/hudi-spark3.3-bundle_2.12/0.13.1/hudi-spark3.3-bundle_2.12-0.13.1.jar --output /opt/bitnami/spark/jars/hudi-spark-bundle-0.13.1.jar

# install required python packages
RUN pip install pyspark

# change working directory for easier PySpark script execution
WORKDIR /opt/bitnami/spark/pyspark