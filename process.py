from pyspark.sql import SparkSession
import pandas as pd
from pyspark.sql.functions import col, expr, concat, countDistinct, to_timestamp, year, count, to_date, month, \
    weekofyear, lit
from pyspark.sql.types import StructType, ArrayType, StringType, StructField, IntegerType, BooleanType, FloatType

# Driver
spark = SparkSession \
    .builder \
    .master('local') \
    .appName('julien') \
    .getOrCreate()

pandas_df1 = pd.read_excel('./dataset/青年大学习.xlsx')
pandas_df2 = pd.read_excel('./dataset/困难认定.xlsx')
spark_df1 = spark.createDataFrame(pandas_df1)
spark_df2 = spark.createDataFrame(pandas_df2)

spark_df1 = spark_df1.select("sn").distinct()
spark_df1 = spark_df1.withColumnRenamed("sn", "id")
spark_df1 = spark_df1.withColumn("name",lit("0").cast(StringType()))
spark_df1 = spark_df1.withColumn("college",lit("数据学院").cast(StringType()))
spark_df1 = spark_df1.withColumn("major",lit("0").cast(StringType()))
spark_df1 = spark_df1.withColumn("node_name",lit("0").cast(StringType()))
spark_df1 = spark_df1.withColumn("late_level",lit(0).cast(IntegerType()))
spark_df1 = spark_df1.withColumn("cheat_level",lit(0).cast(IntegerType()))
spark_df1 = spark_df1.withColumn("poverty_level",lit(0).cast(IntegerType()))
spark_df1 = spark_df1.withColumn("politics_level",lit(0).cast(IntegerType()))
spark_df1 = spark_df1.withColumn("academy_level",lit(0).cast(IntegerType()))
spark_df1 = spark_df1.withColumn("mental_level",lit(0).cast(IntegerType()))
spark_df1 = spark_df1.withColumn("total_grade",lit(0).cast(IntegerType()))

spark_df2 = spark_df2.select("sn","major")

# schema2 = StructType(spark_df1.schema.fields + schema)
# student_df = spark.createDataFrame(spark_df1.rdd, schema2)
# student_df = student_df.withColumn("college", lit("数据学院"))
# for field in schema.fields:
#     field_name = field.name
#     if field_name != "college":
#         student_df = student_df.withColumn(field_name, lit(0))

spark_df1.show(5)

spark_df1.printSchema()