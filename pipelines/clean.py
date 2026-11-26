from connection import get_spark
from pyspark.sql import functions as F

spark = get_spark()

df = spark.table("workspace.bronze.webpages")

cleaned = (
    df
    .withColumn("text", F.trim(F.col("text")))
    .filter(F.col("text").isNotNull())
    .filter(F.length("text") > 0)
    .filter(F.col("label").isin(0, 1))
    .dropDuplicates(["text"])
)

cleaned.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("workspace.silver.webpages")