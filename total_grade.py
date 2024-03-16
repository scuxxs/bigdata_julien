from pyspark.sql import HiveContext
from pyspark.sql.types import StructType, StructField, StringType, FloatType, IntegerType
from pyspark import SparkConf,SparkContext
from pyspark.sql.functions import avg, unix_timestamp, from_unixtime, when, col, sqrt

conf = SparkConf()
sc = SparkContext(conf= conf)

hive_context = HiveContext(sc)

df_student = hive_context.table('student')
df_late = hive_context.table('late')
df_borrow = hive_context.table('borrow')
df_lib = hive_context.table('library')
df_teen = hive_context.table('teenagerLearning')
df_cost = hive_context.table('cost')
df_gate = hive_context.table('gate')
df_net = hive_context.table('net')
df_poverty = hive_context.table('poverty')
# 现在我计算出了以下的值，还有一个student表包含所有学生信息，帮我建立一个展示学生综合表现的df，包括以下字段：
# id, late_time, borrow_time, lib_time, pol_time, cost_time, avg_cost, gate_time, avg_byte, net_time, poor_level
# 注意，有可能在某些字段上，某个id无记录，若无记录则按下述默认值赋值：
# late_time=0, borrow_time=0, lib_time=0, pol_time=0, cost_time=0, avg_cost=0, gate_time=0, avg_byte=0, net_time=0, poor_level=0
# 计算每个 id 的 late 次数
df_late_time = df_late.groupBy('id').count()
df_borrow_time = df_borrow.groupBy('id').count()
df_lib_time = df_lib.filter(df_lib['type'] == '进') \
                           .groupBy('id') \
                           .count()
df_pol_time = df_teen.groupBy('id').count()
df_cost_time = df_cost.groupBy('id').count()
df_avg_cost = df_cost.groupBy('id').agg(avg('amount').alias('avg_amount'))
df_gate_time = df_gate.filter(df_gate['type'] == '进') \
                           .groupBy('id') \
                           .count()
df_avg_byte = df_net.groupBy('id').agg(avg('total_byte').alias('avg_byte'))
df_net_time = df_net.groupBy('id').count()
# # 根据困难程度给定相应的值
# df_poverty = df_poverty.withColumn('poor_level', when(df_poverty['level'] == '不困难', 0)
#                                      .when(df_poverty['level'] == '一般困难', 1)
#                                      .when(df_poverty['level'] == '困难', 2)
#                                      .when(df_poverty['level'] == '特别困难', 3)
#                                      .otherwise(0))
# # 将字符串时间转换为时间戳
# df_net = df_net.withColumn('add_time_ts', unix_timestamp(df_net['add_time'], 'yyyy-MM-dd HH:mm:ss')) \
#                .withColumn('drop_time_ts', unix_timestamp(df_net['drop_time'], 'yyyy-MM-dd HH:mm:ss'))
# # 计算每次上网的时长
# df_net = df_net.withColumn('duration', df_net['drop_time_ts'] - df_net['add_time_ts'])
# # 计算每个 ID 的平均上网时间
# df_avg_duration = df_net.groupBy('id').agg({'duration': 'avg'})

# 按照 id 进行左连接
df_performance = df_student.join(df_late_time, 'id', 'left') \
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

# 定义评价指标的权重
weights = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
# 计算每个指标的平方和
df_performance_square_sum = df_performance.select([(col(col_name) ** 2).alias(col_name + '_square_sum')
                                                    for col_name in df_performance.columns])
# 计算每个指标的平方和的平方根
df_performance_square_root = df_performance_square_sum.select([sqrt(col(col_name)).alias(col_name + '_square_root')
                                                                for col_name in df_performance_square_sum.columns])
# 计算正负理想解
positive_ideal_solution = df_performance_square_root.select([(col(col_name) * weight).alias(col_name)
                                                             for col_name, weight in zip(df_performance_square_root.columns, weights)]) \
                                                     .agg(*[(col_name, 'max') if col_name in ['borrow_time', 'lib_time', 'pol_time']
                                                            else (col_name, 'min') for col_name in df_performance_square_root.columns])

negative_ideal_solution = df_performance_square_root.select([(col(col_name) * weight).alias(col_name)
                                                             for col_name, weight in zip(df_performance_square_root.columns, weights)]) \
                                                     .agg(*[(col_name, 'min') if col_name in ['borrow_time', 'lib_time', 'pol_time']
                                                            else (col_name, 'max') for col_name in df_performance_square_root.columns])
# 计算每个学生到正负理想解的距离
df_distance = df_performance_square_root.select([(col(col_name) - pos_ideal_sol[col_name]) ** 2
                                                 for col_name, pos_ideal_sol in zip(positive_ideal_solution.columns, positive_ideal_solution.first())]) \
                                        .select([(col(col_name) + neg_ideal_sol[col_name]) ** 2
                                                  for col_name, neg_ideal_sol in zip(negative_ideal_solution.columns, negative_ideal_solution.first())]) \
                                        .select([sum(col(col_name)).alias(col_name)
                                                  for col_name in df_performance_square_root.columns])
# 计算相对权重
df_relative_weights = df_distance.select([(neg_ideal_sol[col_name] / (neg_ideal_sol[col_name] + pos_ideal_sol[col_name])).alias(col_name + '_relative_weight')
                                          for col_name, neg_ideal_sol, pos_ideal_sol in zip(df_distance.columns, negative_ideal_solution.first(), positive_ideal_solution.first())])
# 计算总得分
df_total_grade = df_relative_weights.select([sum(col(col_name) * weight).alias('total_grade')
                                             for col_name, weight in zip(df_relative_weights.columns, weights)])
# 将得分归一化至0-100区间内
total_grade_min_max = df_total_grade.agg({'total_grade': 'min'}).collect()[0]['min']
total_grade_max_max = df_total_grade.agg({'total_grade': 'max'}).collect()[0]['max']
df_total_grade_normalized = df_total_grade.select(((col('total_grade') - total_grade_min_max) / (total_grade_max_max - total_grade_min_max) * 100).alias('total_grade_normalized'))

# 将总得分加到原始df_performance的最后一列
df_performance = df_performance.withColumn('total_grade', df_total_grade_normalized['total_grade_normalized'])
# 显示结果
df_performance.show()