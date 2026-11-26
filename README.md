# Databricks Webpage Classifier

A personal project for learning Databricks, PySpark, and Python.

The goal of this project is to build a machine learning model that identifies terms and conditions webpages for use in an existing Firefox extension, which can further identify when a terms and conditions page contains some sort of prize for reading until the end. The model is exported as JSON so the extension's JavaScript can score pages without any Python at runtime.

Originally it was a pretty simple python script, but I thought it would be a good opportunity to learn some of the principles of Databricks and Spark

I originally gave up on the idea of an extension serving the purpose of identifying hidden prizes in terms and conditions pages because I couldn't find enough training data for examples of hidden winning T&C conditions, but I believe now I could use this smaller model to identify when you are on a T&C page, then that would trigger a request to a python server that calls a smatter AI model API that could probably identify it, so you aren't wasting tokens on every webpage you view. 




## Technologies

- Python
- Databricks Connect
- PySpark
- Databricks SQL
- Delta Lake
- scikit-learn

## Learning Goals

- Connect a local Python application to Databricks.
- Create and query tables in Databricks.
- Use PySpark to clean and transform data.
- Understand how to organize a data processing pipeline.
- Train and evaluate a machine learning model.

## Status

Work in progress. Ingestion into the bronze layer is implemented and verified. Cleaning, preparation, training, and export are implemented but not yet run end to end. Next step is automating the pipeline with Databricks Jobs.

`main.py` is a scratch script that counts sample taxi trips; it is not part of the pipeline.