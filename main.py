from databricks.connect import DatabricksSession

spark = DatabricksSession.builder.serverless().getOrCreate()

trip_count = spark.sql(
    "SELECT COUNT(*) AS total FROM samples.nyctaxi.trips"
).collect()[0]["total"]

print(f"There are {trip_count:,} trips in the sample dataset.")