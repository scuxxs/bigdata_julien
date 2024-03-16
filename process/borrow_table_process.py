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
df1 = spark.read.option("sep", "\t").csv("/datacenter/data/借阅.txt").selectExpr("_c0 as id", "_c9 as loandate", "_c6 as returndate", "_c7 as renewtime", "_c8 as recalltime", "_c23 as isbn" )
# df1 = spark.read.option("sep", "\t").csv("/datacenter/data/上网.txt")
df1 = df1.drop_duplicates()
df1 = df1.withColumn("id", col("id").cast("string"))
id_list = df.select("id").rdd.flatMap(lambda x: x).collect()
filtered_df = df1.filter(col("id").isin(id_list))
filtered_df.show(10)
filtered_df.registerTempTable("temp")
hive_context.sql('''
     INSERT INTO TABLE borrow
     SELECT * FROM temp
''')
hive_context.sql("select * from borrow").show()

