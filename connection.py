"""Shared Spark session factory.

Works in two contexts:
  * inside a Databricks job/notebook - reuse the already-active session
  * locally - connect to the workspace with Databricks Connect (serverless)
"""

from databricks.connect import DatabricksSession


def get_spark():
    try:
        from pyspark.sql import SparkSession

        active = SparkSession.getActiveSession()
        if active is not None:
            return active
    except Exception:
        pass

    return DatabricksSession.builder.serverless().getOrCreate()