-- Step 3: Create Databricks schemas (medallion architecture)
-- These are the SQL equivalents of the statements run by `python -m pipelines.setup`.
-- The `workspace` catalog must already exist.

-- Bronze: raw webpage text and classification labels.
CREATE SCHEMA IF NOT EXISTS workspace.bronze;

-- Silver: cleaned text, validated labels, duplicates removed.
CREATE SCHEMA IF NOT EXISTS workspace.silver;

-- Gold: datasets ready for model training and evaluation.
CREATE SCHEMA IF NOT EXISTS workspace.gold;
