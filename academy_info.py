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
# 现在我计算出了以下的值，还有一个student表包含所有学生信息，帮我建立一个df叫academy_info，id是主键，包括以下字段：
# id, late_time, borrow_time, renewtime_sum, lib_time, pol_time, gate_time, net_time, avg_byte
# 注意，有可能在某些字段上，某个id无记录，若无记录则按下述默认值赋值：
# late_time=0, borrow_time=0, renewtime_sum=0, lib_time=0, pol_time=0, gate_time=0, net_time=0, avg_byte=0

# 晚归次数
df_late_time = df_late.groupBy('id').count()
# 借书次数
df_borrow_time = df_borrow.groupBy('id').count()
df_renewtime_sum = df_borrow.groupBy('id').agg(sum('renewtime').alias('total_renewtime'))

# 图书馆次数
df_lib_time = df_lib.filter(df_lib['type'] == '进') \
                           .groupBy('id') \
                           .count()
# 青年大学习
df_pol_time = df_teen.groupBy('id').count()
# '进'校门次数的记录
df_gate_time = df_gate.filter(df_gate['type'] == '进') \
                           .groupBy('id') \
                           .count()
# 上网次数
df_net_time = df_net.groupBy('id').count()
df_avg_byte = df_net.groupBy('id').agg(avg('total_byte').alias('avg_byte'))

# 设置默认值
default_values = {
    'late_time': 0,
    'borrow_time': 0,
    'renewtime_sum': 0,
    'lib_time': 0,
    'pol_time': 0,
    'gate_time': 0,
    'net_time': 0,
    'avg_byte': 0
}

# 合并 DataFrame
academy_info = df_student
# 合并晚归次数
academy_info = academy_info.join(df_late_time, 'id', 'left').fillna(default_values['late_time'], subset=['count'])
# 合并借书次数
academy_info = academy_info.join(df_borrow_time, 'id', 'left').fillna(default_values['borrow_time'], subset=['count'])
# 合并续借总次数
academy_info = academy_info.join(df_renewtime_sum, 'id', 'left').fillna(default_values['renewtime_sum'], subset=['total_renewtime'])
# 合并图书馆次数
academy_info = academy_info.join(df_lib_time, 'id', 'left').fillna(default_values['lib_time'], subset=['count'])
# 合并青年大学习次数
academy_info = academy_info.join(df_pol_time, 'id', 'left').fillna(default_values['pol_time'], subset=['count'])
# 合并校门进入次数
academy_info = academy_info.join(df_gate_time, 'id', 'left').fillna(default_values['gate_time'], subset=['count'])
# 合并上网次数
academy_info = academy_info.join(df_net_time, 'id', 'left').fillna(default_values['net_time'], subset=['count'])
# 合并平均上网流量
academy_info = academy_info.join(df_avg_byte, 'id', 'left').fillna(default_values['avg_byte'], subset=['avg_byte'])
# 显示结果
academy_info.show()