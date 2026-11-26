# Databricks Webpage Classifier

A personal project for learning Databricks, PySpark, and Python.

The goal of this project was to build a machine learning model that identifies terms and conditions webpages for use in an existing Firefox extension, which can further identify when a terms and conditions page contains some sort of prize for reading until the end. The model is exported as JSON so the extension's JavaScript can score pages without any Python at runtime.

Originally it was a pretty simple python script, but I thought it would be a good opportunity to learn some of the principles of Databricks and Spark, so I've ported it to use those as well. It extracts files, transforms them with databricks compute, then loads a model for use in the extension. 

I originally gave up on the idea of an extension serving the purpose of identifying hidden prizes in terms and conditions pages because I couldn't find enough training data for examples of hidden winning T&C conditions, but I believe now I could use this smaller model to identify when you are on a T&C page, then that would trigger a request to a python server that calls a smatter AI model API that could probably identify it, so you aren't wasting tokens on every webpage you view. Though really there's nothing here specific to T&C. This could be used to train any model that finds a positive or negative match.

## Running

Update the documents in `data/pos` and `data/neg`, then run this command:

```bash
./scripts/refresh.sh
```

It mirrors both folders into the bronze Volume (removing remote files you
deleted locally), deploys the bundle, runs the job on Databricks, and downloads
the new `models/model.json`.

Under the hood:

```bash
databricks fs rm -r dbfs:/Volumes/workspace/bronze/raw/pos
databricks fs cp -r data/pos dbfs:/Volumes/workspace/bronze/raw/pos
# ... same for data/neg
databricks bundle deploy -t dev
databricks bundle run webpage_classifier -t dev
databricks fs cp --overwrite \
  dbfs:/Volumes/workspace/gold/artifacts/model.json ./models/model.json
```


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

Work in progress. The full pipeline (ingest → clean → prepare → train → export)
runs as an on-demand Databricks job and produces `models/model.json`.
Copying that file into the browser extension is still a manual step.

`main.py` is a scratch script that counts sample taxi trips; it is not part of the pipeline.