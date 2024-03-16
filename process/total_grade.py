%pyspark
from pyspark.sql import HiveContext
from pyspark.sql.types import StructType, StructField, StringType, FloatType, IntegerType
from pyspark import SparkConf,SparkContext
from pyspark.sql import functions as fn
from pyspark.sql.functions import avg, unix_timestamp, from_unixtime, when, col, sqrt

hive_context = HiveContext(sc)

df_student = hive_context.table('student')
df_late = hive_context.table('late')
df_borrow = hive_context.table('borrow')
df_lib = hive_context.table('library')
df_teen = hive_context.table('teenagerlearning')
df_cost = hive_context.table('cost')
df_gate = hive_context.table('gate')
df_net = hive_context.table('net')
df_poverty = hive_context.table('poverty')
# 现在我计算出了以下的值，还有一个student表包含所有学生信息，帮我建立一个展示学生综合表现的df，包括以下字段：
# id, late_time, borrow_time, lib_time, pol_time, cost_time, avg_cost, gate_time, avg_byte, net_time, poor_level
# 注意，有可能在某些字段上，某个id无记录，若无记录则按下述默认值赋值：
# late_time=0, borrow_time=0, lib_time=0, pol_time=0, cost_time=0, avg_cost=0, gate_time=0, avg_byte=0, net_time=0, poor_level=0
# 计算每个 id 的 late 次数
df_late_time = df_late.groupBy('id').count().withColumnRenamed('count', 'late_time')
df_late_time.show(5)
df_lib.show(5)

%pyspark
df_borrow_time = df_borrow.groupBy('id').count().withColumnRenamed('count', 'borrow_time')
df_lib.show(5)
df_teen.show(5)
df_lib_time = df_lib.filter(df_lib['record_id'] == '进') \
                           .groupBy('id') \
                           .count().withColumnRenamed('count', 'lib_time')
df_pol_time = df_teen.groupBy('id').count().withColumnRenamed('count', 'pol_time')

df_borrow_time.show(5)
df_lib_time.show(5)
df_pol_time.show(5)

%pyspark
df_cost_time = df_cost.groupBy('id').count().withColumnRenamed('count', 'cost_time')
df_avg_cost = df_cost.groupBy('id').agg(avg('amount').alias('avg_cost'))
df_gate_time = df_gate.filter(df_gate['type'] == '进') \
                           .groupBy('id') \
                           .count().withColumnRenamed('count', 'gate_time')

df_cost_time.show(5)
df_avg_cost.show(5)
df_gate_time.show(5)

%pyspark
df_avg_byte = df_net.groupBy('id').agg(avg('total_byte').alias('avg_byte'))
df_net_time = df_net.groupBy('id').count().withColumnRenamed('count', 'net_time')
df_avg_byte.show(5)
df_net_time.show(5)

% pyspark

# 按照 id 进行左连接
df_performance = df_student.select('id')
df_performance = df_performance.join(df_late_time, 'id', 'left') \
    .join(df_borrow_time, 'id', 'left') \
    .join(df_lib_time, 'id', 'left') \
    .join(df_pol_time, 'id', 'left') \
    .join(df_cost_time, 'id', 'left') \
    .join(df_avg_cost, 'id', 'left') \
    .join(df_gate_time, 'id', 'left') \
    .join(df_avg_byte, 'id', 'left') \
    .join(df_net_time, 'id', 'left')

# 填充缺失值为默认值
df_performance = df_performance.fillna(0, subset=['late_time', 'borrow_time', 'lib_time', 'pol_time', 'cost_time',
                                                  'avg_cost', 'gate_time', 'avg_byte', 'net_time'])


# 定义归一化函数
def normalize(column, max_val, min_val):
    return (column - min_val) / (max_val - min_val)


# 获取每列的最大值和最小值
max_values = df_performance.agg(*(F.max(col_name).alias(col_name) for col_name in columns_to_normalize)).collect()[0]
min_values = df_performance.agg(*(F.min(col_name).alias(col_name) for col_name in columns_to_normalize)).collect()[0]

# 对每一列进行归一化操作
for column in columns_to_normalize:
    max_val = max_values[column]
    min_val = min_values[column]
    df_performance = df_performance.withColumn(column, F.udf(lambda x: normalize(x, max_val, min_val))(col(column)))

# 选择需要的列并显示结果
result_df = df_performance.select('id', *[column for column in columns_to_normalize])
result_df.show()
df_performance.show(5)

%pyspark

need_columns = ['late_time', 'borrow_time', 'lib_time', 'pol_time', 'cost_time',
                                                  'avg_cost', 'gate_time', 'avg_byte', 'net_time']


df_performance = result_df

# 定义评价指标的权重
weights = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
# 计算每个指标的平方和
df_performance_square_sum = df_performance.select([(col(col_name) ** 2).alias(col_name + '_square_sum')
                                                    for col_name in need_columns])
# 计算每个指标的平方和的平方根
df_performance_square_root = df_performance_square_sum.select([sqrt(col(col_name)).alias(col_name + '_square_root')
                                                                for col_name in df_performance_square_sum.columns])
# # 计算正负理想解
# positive_ideal_solution = df_performance_square_root.select([(col(col_name) * weight).alias(col_name)
#                                                              for col_name, weight in zip(df_performance_square_root.columns, weights)]) \
#                                                      .agg(*[(fn.max(col_name).alias(col_name)) if col_name in ['borrow_time', 'lib_time', 'pol_time']
#                                                             else (fn.min(col_name).alias(col_name)) for col_name in df_performance_square_root.columns])

from pyspark.sql.functions import lit, min, max

# 计算 borrow_time、lib_time、pol_time 的最大值
borrow_time_max = df_performance.agg(max('borrow_time')).collect()[0][0]
lib_time_max = df_performance.agg(max('lib_time')).collect()[0][0]
pol_time_max = df_performance.agg(max('pol_time')).collect()[0][0]

# 创建 DataFrame positive_ideal_solution
positive_ideal_solution = df_performance.select(
    lit(min(df_performance['late_time'])).alias('late_time'),
    lit(borrow_time_max).alias('borrow_time'),
    lit(lib_time_max).alias('lib_time'),
    lit(pol_time_max).alias('pol_time'),
    lit(min(df_performance['cost_time'])).alias('cost_time'),
    lit(min(df_performance['avg_cost'])).alias('avg_cost'),
    lit(min(df_performance['gate_time'])).alias('gate_time'),
    lit(min(df_performance['avg_byte'])).alias('avg_byte'),
    lit(min(df_performance['net_time'])).alias('net_time')
)


# 显示结果
positive_ideal_solution.show()

%pyspark

borrow_time_min = df_performance.agg(min('borrow_time')).collect()[0][0]
lib_time_min = df_performance.agg(min('lib_time')).collect()[0][0]
pol_time_min = df_performance.agg(min('pol_time')).collect()[0][0]

# 创建 DataFrame positive_ideal_solution
negative_ideal_solution = df_performance.select(
    lit(max(df_performance['late_time'])).alias('late_time'),
    lit(borrow_time_min).alias('borrow_time'),
    lit(lib_time_min).alias('lib_time'),
    lit(pol_time_min).alias('pol_time'),
    lit(max(df_performance['cost_time'])).alias('cost_time'),
    lit(max(df_performance['avg_cost'])).alias('avg_cost'),
    lit(max(df_performance['gate_time'])).alias('gate_time'),
    lit(max(df_performance['avg_byte'])).alias('avg_byte'),
    lit(max(df_performance['net_time'])).alias('net_time')
)
negative_ideal_solution.show()

%pyspark
from pyspark.sql.functions import abs

# # 计算每个字段与正理想解的差值
# diff_late_time = abs(df_performance['late_time'] - positive_ideal_solution['late_time'])
# diff_borrow_time = abs(df_performance['borrow_time'] - positive_ideal_solution['borrow_time'])
# diff_lib_time = abs(df_performance['lib_time'] - positive_ideal_solution['lib_time'])
# diff_pol_time = abs(df_performance['pol_time'] - positive_ideal_solution['pol_time'])
# diff_cost_time = abs(df_performance['cost_time'] - positive_ideal_solution['cost_time'])
# diff_avg_cost = abs(df_performance['avg_cost'] - positive_ideal_solution['avg_cost'])
# diff_gate_time = abs(df_performance['gate_time'] - positive_ideal_solution['gate_time'])
# diff_avg_byte = abs(df_performance['avg_byte'] - positive_ideal_solution['avg_byte'])
# diff_net_time = abs(df_performance['net_time'] - positive_ideal_solution['net_time'])

# 计算每个字段与正理想解的差值，并给差值列指定不同的列名
print(df_performance.columns)
print(positive_ideal_solution.columns)
# print(col('df_performance.late_time'))
# print(col('positive_ideal_solution.late_time'))
# df_performance.withColumn('late_diff', abs(df_performance['late_time'] - 0)).show(2)
# df_distance = df_performance.withColumn('late_diff', abs(df_performance['late_time'] - positive_ideal_solution['late_time'])) \
#                             .withColumn('borrow_diff', abs(df_performance['borrow_time'] - positive_ideal_solution['borrow_time'])) \
#                             .withColumn('lib_diff', abs(df_performance['lib_time'] - positive_ideal_solution['lib_time'])) \
#                             .withColumn('pol_diff', abs(df_performance['pol_time'] - positive_ideal_solution['pol_time'])) \
#                             .withColumn('cost_diff', abs(df_performance['cost_time'] - positive_ideal_solution['cost_time'])) \
#                             .withColumn('avg_cost_diff', abs(df_performance['avg_cost'] - positive_ideal_solution['avg_cost'])) \
#                             .withColumn('gate_diff', abs(df_performance['gate_time'] - positive_ideal_solution['gate_time'])) \
#                             .withColumn('avg_byte_diff', abs(df_performance['avg_byte'] - positive_ideal_solution['avg_byte'])) \
#                             .withColumn('net_diff', abs(df_performance['net_time'] - positive_ideal_solution['net_time']))

from pyspark.sql.functions import broadcast

# 广播positive_ideal_solution
# broadcasted_ideal_solution = positive_ideal_solution.crossJoin(lit(1)).drop("1")

# 对df_performance中的每一行都进行计算
df_distance = df_performance.crossJoin(positive_ideal_solution)\
                            .withColumn('late_diff', abs(df_performance['late_time'] - positive_ideal_solution['late_time'])) \
                            .withColumn('borrow_diff', abs(df_performance['borrow_time'] - positive_ideal_solution['borrow_time'])) \
                            .withColumn('lib_diff', abs(df_performance['lib_time'] - positive_ideal_solution['lib_time'])) \
                            .withColumn('pol_diff', abs(df_performance['pol_time'] - positive_ideal_solution['pol_time'])) \
                            .withColumn('cost_diff', abs(df_performance['cost_time'] - positive_ideal_solution['cost_time'])) \
                            .withColumn('avg_cost_diff', abs(df_performance['avg_cost'] - positive_ideal_solution['avg_cost'])) \
                            .withColumn('gate_diff', abs(df_performance['gate_time'] - positive_ideal_solution['gate_time'])) \
                            .withColumn('avg_byte_diff', abs(df_performance['avg_byte'] - positive_ideal_solution['avg_byte'])) \
                            .withColumn('net_diff', abs(df_performance['net_time'] - positive_ideal_solution['net_time']))

# 显示结果
df_distance.show(2)
# # 计算总距离
df_distance = df_distance.withColumn('pos_distance',
                                 (df_distance['late_diff'] + df_distance['borrow_diff'] + df_distance['lib_diff'] +
                                  df_distance['pol_diff'] + df_distance['cost_diff'] + df_distance['avg_cost_diff'] +
                                  df_distance['gate_diff'] + df_distance['avg_byte_diff'] + df_distance['net_diff'])) \
                          .select('id', 'pos_distance')

# # 显示结果
df_distance.show()

%pyspark
df_distance_neg = df_performance.crossJoin(negative_ideal_solution)\
                            .withColumn('late_diff1', abs(df_performance['late_time'] - negative_ideal_solution['late_time'])) \
                            .withColumn('borrow_diff1', abs(df_performance['borrow_time'] - negative_ideal_solution['borrow_time'])) \
                            .withColumn('lib_diff1', abs(df_performance['lib_time'] - negative_ideal_solution['lib_time'])) \
                            .withColumn('pol_diff1', abs(df_performance['pol_time'] - negative_ideal_solution['pol_time'])) \
                            .withColumn('cost_diff1', abs(df_performance['cost_time'] - negative_ideal_solution['cost_time'])) \
                            .withColumn('avg_cost_diff1', abs(df_performance['avg_cost'] - negative_ideal_solution['avg_cost'])) \
                            .withColumn('gate_diff1', abs(df_performance['gate_time'] - negative_ideal_solution['gate_time'])) \
                            .withColumn('avg_byte_diff1', abs(df_performance['avg_byte'] - negative_ideal_solution['avg_byte'])) \
                            .withColumn('net_diff1', abs(df_performance['net_time'] - negative_ideal_solution['net_time']))
df_distance_neg = df_distance_neg.withColumn('neg_distance',
                                 (df_distance_neg['late_diff1'] + df_distance_neg['borrow_diff1'] + df_distance_neg['lib_diff1'] +
                                  df_distance_neg['pol_diff1'] + df_distance_neg['cost_diff1'] + df_distance_neg['avg_cost_diff1'] +
                                  df_distance_neg['gate_diff1'] + df_distance_neg['avg_byte_diff1'] + df_distance_neg['net_diff1'])) \
                         .select('id', 'neg_distance')
df_distance_neg.show(10)
# df_distance = df_distance.select('id', 'pos_distance',
#                                  (df_distance['late_diff1'] + df_distance['borrow_diff1'] + df_distance['lib_diff1'] +
#                                   df_distance['pol_diff1'] + df_distance['cost_diff1'] + df_distance['avg_cost_diff1'] +
#                                   df_distance['gate_diff1'] + df_distance['avg_byte_diff1'] + df_distance['net_diff1']).alias('neg_distance'))

%pyspark
df_distance = df_distance.join(df_distance_neg, 'id', 'left')
df_distance.show(5)

%pyspark
# 找到grade列的最大值和最小值
max_values = df_distance.agg(F.max("grade").alias("max_grade")).collect()[0]["max_grade"]
min_values = df_distance.agg(F.min("grade").alias("min_grade")).collect()[0]["min_grade"]

# 使用UDF进行归一化操作
def normalize_to_100(value, max_val, min_val):
    return ((value - min_val) / (max_val - min_val)) * 100

# 注册UDF
normalize_to_100_udf = F.udf(normalize_to_100, FloatType())

# 执行归一化操作并将结果存储到新的列中
df_distance = df_distance.withColumn("grade", normalize_to_100_udf(col("grade"), F.lit(max_values), F.lit(min_values)))

# 显示结果
df_distance.show()

%pyspark
from pyspark.sql import HiveContext
from pyspark.sql.functions import col, expr, concat, countDistinct, to_timestamp, year, count, to_date, month, \
    weekofyear, lit, when
from pyspark.sql.types import StructType, ArrayType, StringType, StructField, IntegerType, BooleanType, FloatType

# 删除 df_student 中的 grade 列
df_student = df_student.drop('total_grade')

# 使用 id 列进行连接，并选择 df_distance 中的 grade 列
df_student_with_grade = df_student.join(df_distance.select('id', 'grade'), on='id', how='left')
df_student_with_grade = df_student_with_grade.withColumnRenamed("grade","total_grade")

# 显示结果
df_student_with_grade.show()


# filtered_df.registerTempTable("temp")
# hive_context.sql('''
#     INSERT INTO TABLE late
#     SELECT * FROM temp
# ''')
# hive_context.sql("select * from late").show()




