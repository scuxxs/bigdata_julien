from pyspark.sql import HiveContext
from pyspark.sql.types import StructType, StructField, StringType, FloatType, IntegerType
from pyspark import SparkConf,SparkContext
from pyspark.sql.functions import avg, unix_timestamp, from_unixtime, when, col, sqrt, to_date, count

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
# 指标计算
# 现在我计算出了以下的值，还有一个student表包含所有学生信息，帮我建立一个df叫mental_info，id是主键，包括以下字段：
# id, late_time, borrow_time, lib_time, gate_time, cost_time, avg_cost, net_time, poor_level, avg_duration
# 注意，有可能在某些字段上，某个id无记录，若无记录则按下述默认值赋值：
# late_time=0, borrow_time=0, lib_time=0, gate_time=0, cost_time=0, avg_cost=0, net_time=0, poor_level=0, avg_duration=0

# 晚归次数
df_late_time = df_late.groupBy('id').count()
# 借书次数
df_borrow_time = df_borrow.groupBy('id').count()
# 图书馆次数
df_lib_time = df_lib.filter(df_lib['type'] == '进') \
                           .groupBy('id') \
                           .count()
# '进'校门次数的记录
df_gate_time = df_gate.filter(df_gate['type'] == '进') \
                           .groupBy('id') \
                           .count()
# 消费次数
df_cost_time = df_cost.groupBy('id').count()
# 平均消费
df_avg_cost = df_cost.groupBy('id').agg(avg('amount').alias('avg_amount'))
# 上网次数
df_net_time = df_net.groupBy('id').count()
# 根据困难程度给定相应的值
df_poverty = df_poverty.withColumn('poor_level', when(df_poverty['level'] == '不困难', 0)
                                     .when(df_poverty['level'] == '一般困难', 1)
                                     .when(df_poverty['level'] == '困难', 2)
                                     .when(df_poverty['level'] == '特别困难', 3)
                                     .otherwise(0))
# 将字符串时间转换为时间戳
df_net = df_net.withColumn('add_time_ts', unix_timestamp(df_net['add_time'], 'yyyy-MM-dd HH:mm:ss')) \
               .withColumn('drop_time_ts', unix_timestamp(df_net['drop_time'], 'yyyy-MM-dd HH:mm:ss'))
# 计算每次上网的时长
df_net = df_net.withColumn('duration', df_net['drop_time_ts'] - df_net['add_time_ts'])
# 计算每个 ID 的平均上网时间
df_avg_duration = df_net.groupBy('id').agg({'duration': 'avg'})

# 设置默认值
default_values = {
    'late_time': 0,
    'borrow_time': 0,
    'lib_time': 0,
    'gate_time': 0,
    'cost_time': 0,
    'avg_cost': 0,
    'net_time': 0,
    'poor_level': 0,
    'avg_duration': 0
}

# 合并 DataFrame
mental_info = df_student
# 合并晚归次数
mental_info = mental_info.join(df_late_time, 'id', 'left').fillna(default_values['late_time'], subset=['count'])
# 合并借书次数
mental_info = mental_info.join(df_borrow_time, 'id', 'left').fillna(default_values['borrow_time'], subset=['count'])
# 合并图书馆次数
mental_info = mental_info.join(df_lib_time, 'id', 'left').fillna(default_values['lib_time'], subset=['count'])
# 合并校门进入次数
mental_info = mental_info.join(df_gate_time, 'id', 'left').fillna(default_values['gate_time'], subset=['count'])
# 合并消费次数
mental_info = mental_info.join(df_cost_time, 'id', 'left').fillna(default_values['cost_time'], subset=['count'])
# 合并平均消费
mental_info = mental_info.join(df_avg_cost, 'id', 'left').fillna(default_values['avg_cost'], subset=['avg_amount'])
# 合并上网次数
mental_info = mental_info.join(df_net_time, 'id', 'left').fillna(default_values['net_time'], subset=['count'])
# 合并贫困程度
mental_info = mental_info.join(df_poverty, 'id', 'left').fillna(default_values['poor_level'], subset=['poor_level'])
# 合并平均上网时长
mental_info = mental_info.join(df_avg_duration, 'id', 'left').fillna(default_values['avg_duration'], subset=['avg(duration)'])
# 重新命名平均上网时长字段
mental_info = mental_info.withColumnRenamed('avg(duration)', 'avg_duration')
# 显示结果
mental_info.show()