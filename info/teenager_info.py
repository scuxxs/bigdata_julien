%pyspark

df_teen = hive_context.table('teenagerlearning')
df_pol_time = df_teen.groupBy('id').count().withColumnRenamed('count', 'pol_time')

df_pol_time.show()
# df_poverty = df_poverty.withColumn('poor_level', when(df_poverty['level'] == '不困难', 0)
#                                      .when(df_poverty['level'] == '一般困难', 1)
#                                      .when(df_poverty['level'] == '困难', 2)
#                                      .when(df_poverty['level'] == '特别困难', 3)
#                                      .otherwise(0)).select('id', 'poor_level')
%pyspark
from pyspark.sql import functions as F
max_values = df_pol_time.agg(*(F.max(col_name).alias(col_name) for col_name in ['pol_time'])).collect()[0]
min_values = df_pol_time.agg(*(F.min(col_name).alias(col_name) for col_name in ['pol_time'])).collect()[0]

%pyspark
df_pol_time = df_pol_time.withColumn('politics_level', when(df_pol_time['pol_time'] < 19 , 4)
                                     .when((df_pol_time['pol_time'] < 38) & (df_pol_time['pol_time'] >= 19), 3)
                                     .when((df_pol_time['pol_time'] < 57) & (df_pol_time['pol_time'] >= 38), 2)
                                     .when((df_pol_time['pol_time'] < 76) & (df_pol_time['pol_time'] >= 57), 1)
                                     .otherwise(0)).select('id', 'politics_level')

%pyspark
df_student = hive_context.table('student')
from pyspark.sql import HiveContext
from pyspark.sql.functions import col, expr, concat, countDistinct, to_timestamp, year, count, to_date, month, \
    weekofyear, lit, when
from pyspark.sql.types import StructType, ArrayType, StringType, StructField, IntegerType, BooleanType, FloatType

# 删除 df_student 中的 grade 列
df_student = df_student.drop('politics_level')

# 使用 id 列进行连接，并选择 df_distance 中的 grade 列
df_student_with_politics_level = df_student.join(df_pol_time, on='id', how='left')
df_student_with_politics_level = df_student_with_politics_level.fillna(4, subset=['politics_level'])
# 显示结果
df_student_with_politics_level.show(10)

%pyspark
df_student_with_politics_level.registerTempTable("temp")
hive_context.sql('''
    INSERT INTO TABLE student_tmp3
    SELECT * FROM temp
''')
hive_context.sql("select * from student_tmp3").show()
