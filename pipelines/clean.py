import os
import sys

# Make the repo root importable so `from connection import get_spark` works.
# Locally the script is a normal file (__file__ exists); inside a Databricks
# job it may be exec()'d, so fall back to argv[0] and finally cwd.
def _repo_root() -> str:
    for anchor in (globals().get("__file__"), sys.argv[0] if sys.argv else None):
        if anchor:
            root = os.path.dirname(os.path.dirname(os.path.abspath(anchor)))
            if os.path.isfile(os.path.join(root, "connection.py")):
                return root
    d = os.getcwd()
    while True:
        if os.path.isfile(os.path.join(d, "connection.py")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return os.getcwd()
        d = parent


sys.path.insert(0, _repo_root())

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