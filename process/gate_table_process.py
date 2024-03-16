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
df1 = spark.read.option("sep", "\t").csv("/datacenter/data/校门门禁.txt").selectExpr("_c0 as id", "_c3 as type", "_c4 as record_time", "_c5 as is_vocation")
df1 = df1.drop_duplicates()
df1 = df1.withColumn("id", col("id").cast("string"))
df1.printSchema()
id_list = df.select("id").rdd.flatMap(lambda x: x).collect()
filtered_df = df1.filter(col("id").isin(id_list))
filtered_df.registerTempTable("temp")
hive_context.sql('''
    INSERT INTO TABLE gate
    SELECT * FROM temp
''')
hive_context.sql("select * from gate").show()

