from connection import get_spark

spark = get_spark()

spark.sql("CREATE SCHEMA IF NOT EXISTS workspace.bronze")
spark.sql("CREATE SCHEMA IF NOT EXISTS workspace.silver")
spark.sql("CREATE SCHEMA IF NOT EXISTS workspace.gold")

print("Schemas created successfully.")