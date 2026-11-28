# Databricks Webpage Classifier

A personal project for learning Databricks, PySpark, and Python.

The goal of this project was to build a machine learning model that identifies terms and conditions webpages for use in an existing Firefox extension, which can further identify when a terms and conditions page contains some sort of prize for reading until the end. The model is exported as JSON so the extension's JavaScript can score pages without any Python at runtime.

Originally it was a pretty simple python script, but I thought it would be a good opportunity to learn some of the principles of Databricks and Spark, so I've ported it to use those as well. It extracts files, transforms them with databricks compute, then loads a model for use in the extension. 

I originally gave up on the idea of an extension serving the purpose of identifying hidden prizes in terms and conditions pages because I couldn't find enough training data for examples of hidden winning T&C conditions, but I believe now I could use this smaller model to identify when you are on a T&C page, then that would trigger a request to a python server that calls a smarter AI model API that could probably identify it, so you aren't wasting tokens detecting hidden prizes on every webpage you view. Though really there's nothing here specific to T&C. This could be used to train any model that finds a binary match.

## Running

Update the documents in `data/pos` and `data/neg`, then run this command:

```bash
./scripts/refresh.sh
```

It mirrors both folders into the bronze Volume (removing remote files you
deleted locally), deploys the bundle, runs the job on Databricks, and downloads
the new `models/model.json`.

If `data/pos` and `data/neg` don't exist, the script falls back to the small
synthetic corpus in `data/sample/`, so a fresh clone runs end to end without
your own documents.

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


## Scope and limitations

This project was developed as a hands-on introduction to Databricks, Apache Spark, and data engineering rather than as a production-scale machine learning system. The dataset is small enough to process on a single machine, so distributed computing is not strictly necessary. The primary objective was to gain practical experience with the Databricks platform, medallion architecture, pipeline orchestration, and deployment.

The current implementation makes several assumptions for simplicity:

- Combined file size must be small because ingest can out of memory the driver because every document is in a list and uploading the files is a bottle neck because it's one request from local machine. 
- Assumes each training document is one txt file, an artifact of the original: Having each training document be 1 txt file is inefficient. It could make use of Parquet files
- Training time is single core; Spark ML would be better on a production product if justified by business needs. 
- It's just one monolithic run without considering retries and paying for the whole pipeline every time. It could ingest only new files without replacing duplicates or split ingest and train into two jobs that could be retried for example.

At this scale I didn't have to think about Spark operations like shuffles, skew and file layout that wouldn't fit one node. It's primarily the operational side. 


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