from databricks.connect import DatabricksSession


def get_spark():
    return DatabricksSession.builder.serverless().getOrCreate()