import sys, string
import os
import socket
import time
import operator
import boto3
import json
from pyspark.sql import SparkSession
from datetime import datetime

if __name__ == "__main__":
    
    def check_transactions(line):
        try:
            fields = line.split(',')
            if len(fields)!=15:
                return False
            int(fields[3])
            return True
        except:
            return False


    def check_contracts(line):
        try:
            fields = line.split(',')
            if len(fields)!=6:
                return False
            else:
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
    
    
    transactions = spark.sparkContext.textFile("s3a://" + s3_data_repository_bucket + "/ECS765/ethereum-parvulus/transactions.csv")
    contracts = spark.sparkContext.textFile("s3a://" + s3_data_repository_bucket + "/ECS765/ethereum-parvulus/contracts.csv")


    trans = transactions.filter(check_transactions)
    cons = contracts.filter(check_contracts)

    tf = trans.map(lambda x: (x.split(',')[6], int(x.split(',')[7])))
    cf = cons.map(lambda x: (x.split(',')[0],1))
    trans_reducing = tf.reduceByKey(lambda x, y: x + y)
    joining_trans_cons = trans_reducing.join(cf)
    address_value = joining_trans_cons.map(lambda x: (x[0], x[1][0]))
    top10_sc = address_value.takeOrdered(10, key=lambda l: -1*l[1])

    my_bucket_resource = boto3.resource('s3',
            endpoint_url='http://' + s3_endpoint_url,
            aws_access_key_id=s3_access_key_id,
            aws_secret_access_key=s3_secret_access_key)

    now = datetime.now() # current date and time
    date_time = now.strftime("%d-%m-%Y_%H:%M:%S")
    
    filename = 'ethereum_partb_' + date_time + '/top10_smart_contracts.txt'
    
    my_result_object = my_bucket_resource.Object(s3_bucket, filename)
    my_result_object.put(Body=json.dumps(top10_sc))
    
    my_bucket_resource.Object(s3_bucket, filename).download_file(filename)
    
    spark.stop()