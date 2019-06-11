import sys
import pyspark
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType
from pyspark.sql.functions import expr, substring, regexp_replace, col

sc = SparkContext()
ss = SparkSession.builder.appName("500").getOrCreate()

df_load = ss.read.format("csv").option("delimiter", " ").load('hdfs://hadoop-hdfs:9000/data/' + sys.argv[1]);
for i in range(2, len(sys.argv)):
	df_load2 = ss.read.format("csv").option("delimiter", " ").load('hdfs://hadoop-hdfs:9000/data/' + sys.argv[i]);
	df_load = df_load.union(df_load2)

df_load = df_load.withColumn("_c6", df_load["_c6"].cast(IntegerType()))\
	.filter(col("_c6") > 499).filter(col("_c6") < 600).groupby("_c0").count()


df_load = df_load.repartition(1)
df_load.write.format("csv").mode("overwrite").save('hdfs://hadoop-hdfs:9000/log500.csv')

df_check = ss.read.format("csv").load('hdfs://hadoop-hdfs:9000/log500.csv');
df_check.show()