import sys
import pyspark
import re
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType
from pyspark.sql.functions import expr, substring, regexp_replace, col
from hdfs import Config


sc = SparkContext()
ss = SparkSession.builder.appName("time_series").getOrCreate()

df_load = ss.read.format("csv").option("delimiter", " ").load('hdfs://hadoop-hdfs:9000/data/' + sys.argv[1]);
for i in range(2, len(sys.argv)):
	df_load2 = ss.read.format("csv").option("delimiter", " ").load('hdfs://hadoop-hdfs:9000/data/' + sys.argv[i]);
	df_load = df_load.union(df_load2)

df_load = df_load.withColumn("code", df_load[-2])\
	.withColumn("date", substring("_c3", 2 , 11))\
	.withColumn("parsed_date", expr("to_date(date, 'dd/MMM/yyyy')"))\
	.withColumn("method", substring("_c5", 1 , 4))\
	.withColumn("method_clear", regexp_replace(col("method"), '[ "\t]', ''))\
	.filter(col('method_clear').rlike('.*GET|POST|HEAD'))\
	.groupby("parsed_date", "method_clear", "code").count()\
	.filter(col("count") > 9).orderBy("parsed_date", "method_clear", "code")

df_load = df_load.repartition(1)
df_load.write.format("csv").mode("overwrite").save('hdfs://hadoop-hdfs:9000/data//time_series.csv')
df_check = ss.read.format("csv").load('hdfs://hadoop-hdfs:9000/data/time_series.csv');
df_check.show()