import sys
import pyspark
import re
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType
from pyspark.sql.functions import expr, substring, regexp_replace, col, count, size

from pyspark.sql.window import Window

days = lambda i: i * 86400 

sc = SparkContext()
#filtered = sc.textFile(sys.argv[1]).filter(lambda line: 500 < int(line.split(" ")[-2]) < 599).collect()

ss = SparkSession.builder.appName("time_series").getOrCreate()
#df_load = ss.read.csv('hdfs://172.31.0.4:9000/' + sys.argv[1])
df_load = ss.read.format("csv").option("delimiter", " ").load('hdfs://hadoop-hdfs:9000/data/' + sys.argv[1]);
for i in range(2, len(sys.argv)):
	df_load2 = ss.read.format("csv").option("delimiter", " ").load('hdfs://hadoop-hdfs:9000/data/' + sys.argv[i]);
	df_load = df_load.union(df_load2)


df_load = df_load.withColumn("code", df_load[-2])
df_load = df_load.withColumn("code_int", df_load["code"].cast(IntegerType()))

df_load = df_load.withColumn("date", substring("_c3", 2 , 11))
df_load = df_load.withColumn("parsed_date", expr("to_date(date, 'dd/MMM/yyyy')"))

df_load = df_load.filter(df_load["code_int"] > 399).filter(df_load["code_int"] < 600)

#w = Windows.partitionBy(df_load.co).orderBy(df_load.parsed_date)
w = Window.orderBy(df_load.parsed_date.cast("timestamp").cast("long")).rangeBetween(-days(7), 0)

df2 = df_load.withColumn("week_count", count("code_int").over(w))

df2 = df2.repartition(1)
df2.write.format("csv").mode("overwrite").save('hdfs://hadoop-hdfs:9000/data/window.csv')