from pathlib import Path
from connection import get_spark

spark = get_spark()

rows = []

for folder, label in [("pos", 1), ("neg", 0)]:
    for file in Path(f"data/{folder}").glob("*.txt"):
        rows.append({
            "filename": file.name,
            "text": file.read_text(encoding="utf-8"),
            "label": label
        })

df = spark.createDataFrame(rows)

df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("workspace.bronze.webpages")

print(f"Ingested {len(rows)} documents.")