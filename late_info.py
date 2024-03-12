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
df_teen = hive_context.table('teenagerlearning')
df_cost = hive_context.table('cost')
df_gate = hive_context.table('gate')
df_net = hive_context.table('net')
df_poverty = hive_context.table('poverty')
# 指标计算
# 现在我计算出了以下的值，还有一个student表包含所有学生信息，帮我建立一个df叫late_info，id, date是主键，包括以下字段：
# id, date, late_time, lib_time, cost_time, cost_amount, gate_time, is_vacation, poor_level, is_late
# 注意，有可能在某些字段上，某个id无记录，若无记录则按下述默认值赋值：
# late_time=0, lib_time=0, cost_time=0, cost_amount=0, gate_time=0, is_vacation=1, poor_level=0, is_late=0

# 计算每个 ID 的 late 次数
df_late_time = df_late.groupBy('id').count().withColumnRenamed('count', 'late_time')
# 将 record_date 字段转换为日期类型
df_lib = df_lib.withColumn('date', to_date(df_lib['type']))
df_lib.show(10)
# 过滤出 type 为 '进' 的记录
df_enter_records = df_lib.filter(df_lib['record_id'] == '进')
df_enter_records.show(5)
# 根据 id 和 record_date 进行分组，并计算每组的记录数量
df_enter_count_per_day = df_enter_records.groupBy('id', 'date').count().withColumnRenamed('count', 'daily_lib_time')
df_enter_count_per_day.show(5)
# 将 transdate 字段转换为日期类型
df_cost = df_cost.withColumn('date', to_date(df_cost['transdate']))
# 根据 id 和日期进行分组，并计算每组的消费总额
df_daily_cost = df_cost.groupBy('id', 'date').sum('amount').withColumnRenamed('sum(amount)', 'daily_cost')
df_daily_cost.show(5)
# 根据日期进行分组，并计算每天的消费次数
df_daily_cost_count = df_cost.groupBy('id', 'date').agg(count('id').alias('daily_transtime'))
df_daily_cost_count.show(5)
# 将 time 字段转换为日期类型
df_gate = df_gate.withColumn('date', to_date(df_gate['record_time']))
# 过滤出 type 为 '出' 的记录
df_exit_records = df_gate.filter(df_gate['type'] == '出')
# 根据 id 和日期进行分组，并计算每天的出门次数
df_exit_count_per_day = df_exit_records.groupBy('id', 'date').agg(count('id').alias('exit_count'))
df_exit_count_per_day.show(5)
# 根据 id 和日期进行分组，并计算每天是否有请假记录
df_daily_vocation_count = df_gate.filter(df_gate['is_vocation'] == 0) \
                                 .groupBy('id', 'date') \
                                 .agg(count('is_vocation').alias('daily_vocation_count'))
df_daily_vocation_count.show(5)
# 根据困难程度给定相应的值
df_poverty = df_poverty.withColumn('poor_level', when(df_poverty['level'] == '不困难', 0)
                                     .when(df_poverty['level'] == '一般困难', 1)
                                     .when(df_poverty['level'] == '困难', 2)
                                     .when(df_poverty['level'] == '特别困难', 3)
                                     .otherwise(0)).select('id', 'poor_level')
df_poverty.show(5)
# 将 record_date 字段转换为日期类型
df_late = df_late.withColumn('date', to_date(df_late['latedate']))
# 根据 id 和日期进行分组，并统计每个学生每天的晚归次数
df_late_per_day = df_late.groupBy('id', 'date').count().withColumnRenamed('count', 'daily_late_time')
# 将晚归次数大于 1 的记录标记为 1，否则标记为 0
df_late_per_day = df_late_per_day.withColumn('daily_late_time', when(df_late_per_day['daily_late_time'] > 1, 1).otherwise(0))

# 显示结果
df_late_per_day.show(5)
# 设置默认值
default_values = {
    'late_time': 0,
    'daily_lib_time': 0,
    'daily_cost': 0,
    'daily_transtime': 0,
    'exit_count': 0,
    'daily_vocation_count': 0,
    'poor_level': 0,
    'daily_late_time': 0,
}
# 合并 DataFrame
late_info = df_student.select('id', 'name')
# 合并 late_time
late_info = late_info.join(df_late_time, 'id', 'left').fillna(default_values['late_time'], subset=['late_time'])
late_info.show(5)
# 合并 df_enter_count_per_day
late_info = late_info.join(df_enter_count_per_day, ['id'], 'left').fillna(default_values['daily_lib_time'], subset=['daily_lib_time'])
late_info.show(5)
# 合并 df_daily_cost
late_info = late_info.join(df_daily_cost, ['id', 'date'], 'left').fillna(default_values['daily_cost'], subset=['daily_cost'])
# 合并 df_daily_cost_count
late_info = late_info.join(df_daily_cost_count, ['id', 'date'], 'left').fillna(default_values['daily_transtime'], subset=['daily_transtime'])
late_info.show(5)
# 合并 df_exit_count_per_day
late_info = late_info.join(df_exit_count_per_day, ['id', 'time'], 'left').fillna(default_values['gate_time'], subset=['exit_count'])
# 合并 df_is_vacation_per_day
late_info = late_info.join(df_is_vacation_per_day, ['id', 'time'], 'left').fillna(default_values['is_vacation'], subset=['is_vocation'])
# 合并 df_poverty
late_info = late_info.join(df_poverty, 'id', 'left').fillna(default_values['poor_level'], subset=['poor_level'])
# 合并 df_late_per_day
late_info = late_info.join(df_late_per_day, ['id', 'record_date'], 'left').fillna(default_values['is_late'], subset=['count'])
# 重新命名日期字段
late_info = late_info.withColumnRenamed('record_date', 'date')
# 显示结果
late_info.show()
