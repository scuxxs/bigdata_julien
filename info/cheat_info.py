%pyspark
from pyspark.sql import HiveContext
from pyspark.sql.types import StructType, StructField, StringType, FloatType, IntegerType
from pyspark import SparkConf,SparkContext
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

%pyspark
df_cost_time = df_cost.groupBy('id').count().withColumnRenamed('count', 'cost_time')
df_avg_cost = df_cost.groupBy('id').agg(avg('amount').alias('avg_amount'))
df_gate_time = df_gate.filter(df_gate['type'] == '进') \
                           .groupBy('id') \
                           .count().withColumnRenamed('count', 'gate_time')
df_cost_time.show(5)
df_avg_cost.show(5)
df_gate_time.show(5)

%pyspark
# 将字符串时间转换为时间戳
df_net = df_net.withColumn('add_time_ts', unix_timestamp(df_net['add_time'], 'yyyy-MM-dd HH:mm:ss')) \
               .withColumn('drop_time_ts', unix_timestamp(df_net['drop_time'], 'yyyy-MM-dd HH:mm:ss'))
# 计算每次上网的时长
df_net = df_net.withColumn('duration', df_net['drop_time_ts'] - df_net['add_time_ts'])
# 计算每个 ID 的平均上网时间
df_avg_duration = df_net.groupBy('id').agg({'duration': 'avg'})
df_avg_duration.show(5)

%pyspark

# 按照 id 进行左连接
df_performance = df_student.select('id', 'name')
df_performance = df_performance.join(df_late_time, 'id', 'left') \
                               .join(df_cost_time, 'id', 'left') \
                               .join(df_avg_cost, 'id', 'left') \
                               .join(df_gate_time, 'id', 'left') \
                               .join(df_avg_byte, 'id', 'left') \
                               .join(df_net_time, 'id', 'left') \
                               .join(df_avg_duration, 'id', 'left')
# 填充缺失值为默认值
df_performance = df_performance.fillna(0, subset=['late_time', 'cost_time','avg_amount', 'gate_time', 'avg(duration)', 'avg_byte', 'net_time'])
# df_performance = df_performance.fillna(0, subset=['late_time', 'cost_time', 'gate_time', 'avg_byte', 'net_time'])
df_performance.show(5)

% pyspark
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml.clustering import BisectingKMeans

# 构建特征向量
assembler = VectorAssembler().setInputCols(
    ['late_time', 'cost_time', 'avg_amount', 'gate_time', 'avg_byte', 'net_time', 'avg(duration)']).setOutputCol(
    'features')

df_features = assembler.transform(df_performance)
df_features.show(4)

# # 归一化特征
# scaler = StandardScaler(inputCol='features', outputCol='scaledFeatures', withStd=True, withMean=False)
# scalerModel = scaler.fit(df_features)
# scaled_df_features = scalerModel.transform(df_features)

# kmeans = KMeans(k=5, seed=100, maxIter=2, featuresCol='scaledFeatures', predictionCol='predict')
# model = kmeans.fit(scaled_df_features)
# predicted = model.transform(scaled_df_features)
# # 显示聚类结果
# predicted.select('id','name','scaledFeatures', 'predict').show()
# # # 使用层次聚类算法进行聚类
# # kmeans = BisectingKMeans(k=5, seed=100)
# # model = kmeans.fit(scaled_df_features)

# # # 添加聚类结果到原始 DataFrame 中
# # clustered_df = model.transform(scaled_df_features)

# # # 查看聚类结果
# # clustered_df.select('id', 'name', 'features', 'prediction').show()

%pyspark
# # 归一化特征
scaler = StandardScaler(inputCol='features', outputCol='scaledFeatures', withStd=True, withMean=False)
scalerModel = scaler.fit(df_features)
scaled_df_features = scalerModel.transform(df_features)
scaled_df_features.show(4)

%pyspark
# # 使用层次聚类算法进行聚类
kmeans = BisectingKMeans(k=5, seed=100)
model = kmeans.fit(scaled_df_features)

# 添加聚类结果到原始 DataFrame 中
clustered_df = model.transform(scaled_df_features)

# 查看聚类结果
clustered_df.select('id', 'name', 'prediction').show()

%pyspark
from pyspark.sql import functions as F

# 按照聚类结果进行分组，并计算每个聚类簇的平均值
clustered_df_avg = clustered_df.groupBy('prediction').agg(
    F.avg('avg(duration)').alias('avg_duration'),
    F.avg('avg_byte').alias('avg_byte'),
    F.avg('net_time').alias('avg_net_time')
)

# 将三个平均值字段相加
clustered_df_avg = clustered_df_avg.withColumn('sum_of_three_fields',
                                               clustered_df_avg['avg_duration'] +
                                               clustered_df_avg['avg_byte'] +
                                               clustered_df_avg['avg_net_time'])

# 显示每个聚类簇的结果
clustered_df_avg.show()

