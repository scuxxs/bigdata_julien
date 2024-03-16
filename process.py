from pyspark.sql import SparkSession
import pandas as pd
from pyspark.sql.functions import col, expr, concat, countDistinct, to_timestamp, year, count, to_date, month, \
    weekofyear, lit, when
from pyspark.sql.types import StructType, ArrayType, StringType, StructField, IntegerType, BooleanType, FloatType

# Driver
spark = SparkSession \
    .builder \
    .master('local') \
    .appName('julien') \
    .getOrCreate()
columns2_to_read = ["sn", "major_name", "name"]

pandas_df1 = pd.read_excel('./dataset/青年大学习.xlsx')
pandas_df2 = pd.read_excel('./dataset/困难认定.xlsx', usecols=columns2_to_read)

spark_df1 = spark.createDataFrame(pandas_df1)
spark_df2 = spark.createDataFrame(pandas_df2)

"""
处理青年大学习.xlsx和困难认定.xlsx
"""
spark_df1 = spark_df1.select("sn").distinct()
spark_df1 = spark_df1.withColumnRenamed("sn", "id")
spark_df1 = spark_df1.withColumn("name", lit("0").cast(StringType()))
spark_df1 = spark_df1.withColumn("college", lit("数据学院").cast(StringType()))
spark_df1 = spark_df1.withColumn("major", lit("0").cast(StringType()))
spark_df1 = spark_df1.withColumn("node_name", lit("0").cast(StringType()))
spark_df1 = spark_df1.withColumn("late_level", lit(0).cast(IntegerType()))
spark_df1 = spark_df1.withColumn("cheat_level", lit(0).cast(IntegerType()))
spark_df1 = spark_df1.withColumn("poverty_level", lit(0).cast(IntegerType()))
spark_df1 = spark_df1.withColumn("politics_level", lit(0).cast(IntegerType()))
spark_df1 = spark_df1.withColumn("academy_level", lit(0).cast(IntegerType()))
spark_df1 = spark_df1.withColumn("mental_level", lit(0).cast(IntegerType()))
spark_df1 = spark_df1.withColumn("total_grade", lit(0).cast(IntegerType()))

spark_df2 = spark_df2.select("sn", "major_name", "name").distinct()
spark_df2 = spark_df2.withColumnRenamed("sn", "id")
spark_df2 = spark_df2.withColumnRenamed("name", "name2")
spark_df2 = spark_df2.withColumnRenamed("major_name", "major2")
spark_df2.show(5)

joined_df = spark_df2.join(spark_df1, "id", "full_outer")
filled_df = joined_df.withColumn("name",
                                 when(col("name") == "0", col("name2")).otherwise(col("name")))
filled_df = filled_df.withColumn("major",
                                 when(col("major") == "0", col("major2")).otherwise(col("major")))

result1_df = filled_df.drop("major2", "name2")
result1_df = result1_df.withColumn("id", col("id").cast("string"))
result1_df.printSchema()
result1_df.show(5)

"""
加入 上网.txt
"""
columns3_indices_to_read = [0, 1]
pandas_df3 = pd.read_csv('./dataset/上网.txt', sep='\t', header=None, usecols=columns3_indices_to_read)
colu_names_3 = ['id', 'name3']
pandas_df3.columns = colu_names_3
pandas_df3 = pandas_df3.drop_duplicates()
spark_df3 = spark.createDataFrame(pandas_df3)
spark_df3 = spark_df3.distinct()
spark_df3 = spark_df3.withColumn("id", col("id").cast("string"))
joined_df2 = spark_df3.join(result1_df, "id", "full_outer")
joined_df2.show(5)
filled_df2 = joined_df2.withColumn("name",
                                   when(col("name").isNull(), col("name3")).otherwise(col("name")))
result2_df = filled_df2.drop("name3")
