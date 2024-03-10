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
df1 = spark.read.option("sep", "\t").option("header", "true").csv("/datacenter/data/困难认定.txt").selectExpr("sn as id", "result_level as level", "school_year_name as school_year")
# df1 = spark.read.option("sep", "\t").csv("/datacenter/data/上网.txt")
df1 = df1.drop_duplicates()
df1 = df1.withColumn("id", col("id").cast("string"))
id_list = df.select("id").rdd.flatMap(lambda x: x).collect()
filtered_df = df1.filter(col("id").isin(id_list))
filtered_df.registerTempTable("temp")
hive_context.sql('''
     INSERT INTO TABLE poverty
     SELECT * FROM temp
''')
hive_context.sql("select * from poverty").show()