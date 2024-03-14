from pyspark.sql import HiveContext
from pyspark.sql.types import StructType, StructField, StringType, FloatType, IntegerType
from pyspark import SparkConf,SparkContext
from pyspark.sql.functions import avg, unix_timestamp, from_unixtime, when, col, sqrt, to_date, count

conf = SparkConf()
sc = SparkContext(conf= conf)

hive_context = HiveContext(sc)

df_student = hive_context.table('student')

from pyspark.sql.functions import lit

# 创建一个空的 DataFrame
college_df = spark.createDataFrame([], schema="major string, type string, level int, num int")

# 为每种类型和级别创建行，并统计人数
for type in ['late', 'cheat', 'poverty', 'politics', 'academy', 'mental']:
    for level in range(5):  # level 取值范围为 0-4
        type_level_count = df_student.filter(df_student[type + '_level'] == level) \
                                     .groupBy('major') \
                                     .count() \
                                     .withColumnRenamed('count', 'num') \
                                     .withColumn('type', lit(type)) \
                                     .withColumn('level', lit(level))
        college_df = college_df.union(type_level_count.select('major', 'type', 'level', 'num'))

# 展示 DataFrame
college_df.show(50)
