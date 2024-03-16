%pyspark
from pyspark.sql import HiveContext
from pyspark.sql.functions import col, expr, concat, countDistinct, to_timestamp, year, count, to_date, month, \
    weekofyear, lit, when
from pyspark.sql.types import StructType, ArrayType, StringType, StructField, IntegerType, BooleanType, FloatType

# Driver
# spark = SparkSession \
#     .builder \
#     .master('local') \
#     .appName('julien') \
#     .getOrCreate()
hive_context = HiveContext(sc)
columns2_to_read = ['sn', 'major_name', 'name']


pandas_df1 = spark.read.option("header", "true") \
    .option("delimiter", "\t") \
    .option("inferSchema", "true") \
    .csv("/datacenter/data/青年大学习.txt")

pandas_df2 = spark.read.option("header", "true") \
    .option("delimiter", "\t") \
    .option("inferSchema", "true") \
    .csv("/datacenter/data/困难认定.txt") \
    .select(columns2_to_read)


"""
处理青年大学习.xlsx和困难认定.xlsx
"""
spark_df1 = pandas_df1.select("sn").distinct()
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

spark_df2 = pandas_df2.select("sn", "major_name", "name").distinct()
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
处理 上网.txt
"""
# columns3_indices_to_read = [0, 1]
# pandas_df3 = pd.read_csv('/datacenter/data/上网.txt', sep='\t', header=None, usecols=columns3_indices_to_read)
# colu_names_3 = ['id', 'name3']
# pandas_df3.columns = colu_names_3
# pandas_df3 = pandas_df3.drop_duplicates()
columns3_indices_to_read = [0, 1]
pandas_df3 = spark.read.option("sep", "\t").csv("/datacenter/data/上网.txt").selectExpr("_c0 as id", "_c1 as name3")
spark_df3 = pandas_df3.drop_duplicates()
spark_df3 = spark_df3.withColumn("id", col("id").cast("string"))
joined_df2 = spark_df3.join(result1_df, "id", "full_outer")
# joined_df2.show(5)
filled_df2 = joined_df2.withColumn("name",
                                   when((col("name").isNull()) | (col("name") == "0"), col("name3")).otherwise(
                                       col("name")))
# filled_df2.show(5)
result2_df = filled_df2.drop("name3")
# a = result2_df.where(col("id") == "2020080908024").show()

"""
处理实体卡消费.txt
"""

# columns4_indices_to_read = [0, 1]
# pandas_df4 = pd.read_csv('/datacenter/data/实体卡消费.txt', sep='\t', header=None, usecols=columns4_indices_to_read, dtype={0:str})
# colu_names_4 = ['id', 'name4']
# pandas_df4.columns = colu_names_4
# pandas_df4 = pandas_df4.drop_duplicates()
columns4_indices_to_read = [0, 1]
pandas_df4 = spark.read.option("sep", "\t").csv("/datacenter/data/实体卡消费.txt").selectExpr("_c0 as id", "_c1 as name4")
spark_df4 = pandas_df4.drop_duplicates()
spark_df4 = spark_df4.withColumn("id", col("id").cast("string"))
joined_df3 = spark_df4.join(result2_df, "id", "full_outer")
# joined_df3.show(5)
filled_df3 = joined_df3.withColumn("name",
                                   when((col("name").isNull()) | (col("name") == "0"), col("name4")).otherwise(
                                       col("name")))
result3_df = filled_df3.drop("name4")
filled_df3.show(5)
# result3_df.where(col("id") == "2020080908024").show()

"""
处理电子卡消费.txt
"""

columns5_indices_to_read = [0, 3]
pandas_df5 = spark.read.option("sep", "\t").csv("/datacenter/data/电子卡消费.txt").selectExpr("_c0 as id", "_c3 as name5")
spark_df5 = pandas_df5.drop_duplicates()
spark_df5 = spark_df5.withColumn("id", col("id").cast("string"))
joined_df4 = spark_df5.join(result3_df, "id", "full_outer")
# joined_df3.show(5)
filled_df4 = joined_df4.withColumn("name",
                                   when((col("name").isNull()) | (col("name") == "0"), col("name5")).otherwise(
                                       col("name")))
result4_df = filled_df4.drop("name5")
filled_df4.show(5)
# result4_df.where(col("id") == "2020080908024").show()

"""
处理图书馆门禁.txt
"""
pandas_df6 = spark.read.option("sep", "\t").csv("/datacenter/data/图书馆门禁.txt").selectExpr("_c2 as id", "_c3 as name6")
spark_df6 = pandas_df6.drop_duplicates()
spark_df6 = spark_df6.withColumn("id", col("id").cast("string"))
joined_df5 = spark_df6.join(result4_df, "id", "full_outer")
# joined_df3.show(5)
filled_df5 = joined_df5.withColumn("name",
                                   when((col("name").isNull()) | (col("name") == "0"), col("name6")).otherwise(
                                       col("name")))
result5_df = filled_df5.drop("name6")
filled_df5.show(5)
# result5_df.where(col("id") == "2020080908024").show()

"""
处理晚归.txt
"""
pandas_df7 = spark.read.option("sep", "\t").csv("/datacenter/data/晚归.txt").selectExpr("_c0 as id", "_c3 as node")
spark_df7 = pandas_df7.drop_duplicates()
spark_df7 = spark_df7.withColumn("id", col("id").cast("string"))
joined_df6 = spark_df7.join(result5_df, "id", "full_outer")
# joined_df3.show(5)
filled_df6 = joined_df6.withColumn("node_name",
                                   when((col("node_name").isNull()) | (col("node_name") == "0"), col("node")).otherwise(
                                       col("node_name")))
result6_df = filled_df6.drop("node")
# result6_df.where(col("node_name") == "本科4组团").show(5)


result = result6_df.withColumn("college", lit("数据学院").cast(StringType()))
result = result.withColumn("late_level", lit(0).cast(IntegerType()))
result = result.withColumn("cheat_level", lit(0).cast(IntegerType()))
result = result.withColumn("poverty_level", lit(0).cast(IntegerType()))
result = result.withColumn("politics_level", lit(0).cast(IntegerType()))
result = result.withColumn("academy_level", lit(0).cast(IntegerType()))
result = result.withColumn("mental_level", lit(0).cast(IntegerType()))
result = result.withColumn("total_grade", lit(0).cast(IntegerType()))
result_filled = result.fillna("0", subset = ["major"])


# result_filled.where(col("node_name") == "本科4组团").show(5)
result_filled.show(5)

result_filled.registerTempTable("temp")

hive_context.sql('''
    INSERT INTO TABLE student
    SELECT * FROM temp
''')
hive_context.sql("select * from student").show()