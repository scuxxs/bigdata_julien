%pyspark
from pyspark.sql import HiveContext
from pyspark.sql.types import StructType, StructField, StringType, FloatType, IntegerType
from pyspark import SparkConf,SparkContext
from pyspark.sql.functions import avg, unix_timestamp, from_unixtime, when, col, sqrt, to_date, count

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
# 现在我计算出了以下的值，还有一个student表包含所有学生信息，帮我建立一个df叫academy_info，id是主键，包括以下字段：
# id, late_time, borrow_time, renewtime_sum, lib_time, pol_time, gate_time, net_time, avg_byte
# 注意，有可能在某些字段上，某个id无记录，若无记录则按下述默认值赋值：
# late_time=0, borrow_time=0, renewtime_sum=0, lib_time=0, pol_time=0, gate_time=0, net_time=0, avg_byte=0

# 晚归次数
df_late_time = df_late.groupBy('id').count().withColumnRenamed('count', 'late_time')
# 借书次数
df_borrow.show(5)
df_borrow = df_borrow.withColumn("renewtime", col("renewtime").cast("int"))
df_borrow = df_borrow.fillna({"renewtime":0})
df_borrow_time = df_borrow.groupBy('id').count().withColumnRenamed('count', 'borrow_time')
# df_renewtime_sum = df_borrow.groupBy('id').agg(sum('renewtime').alias('total_renewtime'))



df_late_time.show(5)
df_borrow_time.show(5)
# df_renewtime_sum.show(5)

%pyspark
# 图书馆次数
df_lib_time = df_lib.filter(df_lib['record_id'] == '进') \
                           .groupBy('id') \
                           .count().withColumnRenamed('count', 'lib_time')
# 青年大学习
df_pol_time = df_teen.groupBy('id').count().withColumnRenamed('count', 'pol_time')
# '进'校门次数的记录
df_gate_time = df_gate.filter(df_gate['type'] == '进') \
                           .groupBy('id') \
                           .count().withColumnRenamed('count', 'gate_time')
# 上网次数
df_net_time = df_net.groupBy('id').count().withColumnRenamed('count', 'net_time')
df_avg_byte = df_net.groupBy('id').agg(avg('total_byte').alias('avg_byte'))
df_lib_time.show(5)
df_pol_time.show(5)
df_gate_time.show(5)
df_net_time.show(5)
df_avg_byte.show(5)

%pyspark

# 设置默认值
default_values = {
    'late_time': 0,
    'borrow_time': 0,
    'lib_time': 0,
    'pol_time': 0,
    'gate_time': 0,
    'net_time': 0,
    'avg_byte': 0
}

# 合并 DataFrame
academy_info = df_student.select('id', 'name', 'total_grade')
# 合并晚归次数
academy_info = academy_info.join(df_late_time, 'id', 'left').fillna(default_values['late_time'], subset=['late_time'])
# 合并借书次数
academy_info = academy_info.join(df_borrow_time, 'id', 'left').fillna(default_values['borrow_time'], subset=['borrow_time'])
# # 合并续借总次数
# academy_info = academy_info.join(df_renewtime_sum, 'id', 'left').fillna(default_values['renewtime_sum'], subset=['total_renewtime'])
# 合并图书馆次数
academy_info = academy_info.join(df_lib_time, 'id', 'left').fillna(default_values['lib_time'], subset=['lib_time'])
# 合并青年大学习次数
academy_info = academy_info.join(df_pol_time, 'id', 'left').fillna(default_values['pol_time'], subset=['pol_time'])
# 合并校门进入次数
academy_info = academy_info.join(df_gate_time, 'id', 'left').fillna(default_values['gate_time'], subset=['gate_time'])
# 合并上网次数
academy_info = academy_info.join(df_net_time, 'id', 'left').fillna(default_values['net_time'], subset=['net_time'])
# 合并平均上网流量
academy_info = academy_info.join(df_avg_byte, 'id', 'left').fillna(default_values['avg_byte'], subset=['avg_byte'])
# 显示结果
academy_info.show()
print(academy_info.count())

%pyspark
from pyspark.ml.clustering import KMeans
from pyspark.ml.feature import VectorAssembler, StandardScaler

assembler = VectorAssembler().setInputCols(['late_time', 'borrow_time', 'lib_time', 'pol_time', 'gate_time', 'net_time', 'avg_byte']).setOutputCol('features')
academy_info_feature_df = assembler.transform(academy_info)
scaler = StandardScaler(inputCol='features', outputCol='scaledFeatures', withStd=True, withMean=False)
scalerModel = scaler.fit(academy_info_feature_df)
scaled_academy_feature_df = scalerModel.transform(academy_info_feature_df)
scaled_academy_feature_df.show()

%pyspark
kmeans = KMeans(k=5, seed=100, maxIter=2, featuresCol='scaledFeatures', predictionCol='predict')
model = kmeans.fit(scaled_academy_feature_df)
predicted = model.transform(scaled_academy_feature_df)

# 显示聚类结果
predicted.select('id','name','total_grade', 'predict').show()
print(predicted.count())


%pyspark
from pyspark.sql import functions as F

# 按照聚类结果进行分组，并计算每个聚类簇的平均值
clustered_df_avg = predicted.groupBy('predict').agg(
    F.avg('total_grade').alias('avg_grade')
)
clustered_df_avg = clustered_df_avg.orderBy('avg_grade', ascending = False)

%pyspark
academy = predicted.withColumn('academy_level', when(predicted['predict'] == 0 , 4)
                                     .when(predicted['predict'] == 4, 3)
                                     .when(predicted['predict'] == 3, 2)
                                     .when(predicted['predict'] == 1, 1)
                                     .otherwise(0)).select('id', 'academy_level')
academy.show(5)
print(academy.count())
