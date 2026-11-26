# Databricks Webpage Classifier

A personal project for learning Databricks, PySpark, and Python.

The goal of this project is to build a machine learning model that identifies terms and conditions webpages for use in an existing Firefox extension. The model is exported as JSON so the extension's JavaScript can score pages without any Python at runtime.

## Data Pipeline

The project uses a medallion architecture in the `workspace` catalog:

- **Bronze** (`pipelines/ingest.py`): Raw webpage text from `data/pos` and `data/neg`, labeled 1/0.
- **Silver** (`pipelines/clean.py`): Trimmed text, empty rows and duplicate documents removed, invalid labels dropped.
- **Gold** (`pipelines/prepare.py`): Training-ready `text`/`label` data.

Each stage writes a Delta table to its schema: `workspace.bronze.webpages`, `workspace.silver.webpages`, and `workspace.gold.training_data`.

## Model Training and Export

The data lives in Databricks, but training runs locally with scikit-learn:

- `training/train.py` reads `workspace.gold.training_data`, trains a TF-IDF + logistic regression pipeline, and saves `models/model.joblib`.
- `training/export.py` converts that pipeline to `models/model.json`, the format the extension's scorer expects (vocabulary, IDF weights, coefficients, intercept, threshold).

## Project Structure

```
pipelines/   # Databricks stages: setup, ingest, clean, prepare
training/    # train and export the model
models/      # generated artifacts: model.joblib, model.json
sql-script/  # SQL queries, in setup/ and analysis/
data/        # local labeled text files (pos/ and neg/)
connection.py
```

## Usage

```bash
python -m pipelines.setup     # create bronze/silver/gold schemas
python -m pipelines.ingest    # bronze
python -m pipelines.clean     # silver
python -m pipelines.prepare   # gold
python -m training.train      # writes models/model.joblib
python -m training.export     # writes models/model.json
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

Work in progress. Ingestion into the bronze layer is implemented and verified. Cleaning, preparation, training, and export are implemented but not yet run end to end. Next step is automating the pipeline with Databricks Jobs.

`main.py` is a scratch script that counts sample taxi trips; it is not part of the pipeline.