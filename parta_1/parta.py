import sys
import string
import os
import socket
import time
import operator
import boto3
import json
from pyspark.sql import SparkSession
from datetime import datetime

if __name__ == "__main__":

    def check_transaction(line):
        try:
            fields = line.split(',')
            if len(fields) != 15:
                return False
            int(fields[11])
            return True
        except:
            return False

    spark = SparkSession\
        .builder\
        .appName("Ethereum")\
        .getOrCreate()
    s3_data_repository_bucket = os.environ['DATA_REPOSITORY_BUCKET']
    s3_endpoint_url = os.environ['S3_ENDPOINT_URL']+':'+os.environ['BUCKET_PORT']
    s3_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
    s3_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
    s3_bucket = os.environ['BUCKET_NAME']

    hadoopConf = spark.sparkContext._jsc.hadoopConfiguration()
    hadoopConf.set("fs.s3a.endpoint", s3_endpoint_url)
    hadoopConf.set("fs.s3a.access.key", s3_access_key_id)
    hadoopConf.set("fs.s3a.secret.key", s3_secret_access_key)
    hadoopConf.set("fs.s3a.path.style.access", "true")
    hadoopConf.set("fs.s3a.connection.ssl.enabled", "false")

    t = spark.sparkContext.textFile("s3a://" + s3_data_repository_bucket + "/ECS765/ethereum-parvulus/transactions.csv")
    clean_lines = t.filter(check_transaction)

    transactions = clean_lines.map(lambda b: (time.strftime("%m/%Y", time.gmtime(int(b.split(',')[11]))), 1))
    tot_transactions = transactions.reduceByKey(operator.add)

    my_bucket_resource = boto3.resource('s3',
                                        endpoint_url='http://' + s3_endpoint_url,
                                        aws_access_key_id=s3_access_key_id,
                                        aws_secret_access_key=s3_secret_access_key)

    now = datetime.now()
    date_time = now.strftime("%d-%m-%Y_%H:%M:%S")

    filename = 'ethereum_' + date_time + '/transactions_total.txt'

    my_result_object = my_bucket_resource.Object(s3_bucket, filename)
    my_result_object.put(Body=json.dumps(tot_transactions.collect()))

    print(tot_transactions.collect())
    my_bucket_resource.Object(s3_bucket, filename).download_file(filename)

    spark.stop()
