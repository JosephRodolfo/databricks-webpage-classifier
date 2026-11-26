from connection import get_spark

spark = get_spark()

df = spark.table("workspace.silver.webpages")

prepared = df.select("text", "label")

prepared.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("workspace.gold.training_data")