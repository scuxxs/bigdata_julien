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
df = spark.read.table("student")
df1 = spark.read.option("sep", "\t").csv("/datacenter/data/图书馆门禁.txt").selectExpr("_c2 as id", "_c15 as type1", "_c16 as type2", "_c20 as recorddate", "_c0 as record_id")
df1 = df1.drop_duplicates()
df1.printSchema()
df1 = df1.withColumn("id", col("id").cast("string"))

df1 = df1.withColumn("type", when((col("type1") == "进") | (col("type1") == "出"), col("type1"))
                     .otherwise(col("type2")))

df1 = df1.withColumn("type", when((col("type") != "进") & (col("type") != "出"),
                                       when(expr("rand() <= 0.5"), lit("进")).otherwise(lit("出")))
                     .otherwise(col("type")))
df2 = df1.drop("type1")
df2 = df2.drop("type2")
df2.show(4)
id_list = df.select("id").rdd.flatMap(lambda x: x).collect()
filtered_df = df2.filter(col("id").isin(id_list))
filtered_df.registerTempTable("temp")
hive_context.sql('''
    INSERT INTO TABLE library
    SELECT * FROM temp
''')
hive_context.sql("select * from library").show()

