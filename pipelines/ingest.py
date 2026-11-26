import os
import sys
from pathlib import Path

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

spark = get_spark()

rows = []

BASE = Path(sys.argv[1] if len(sys.argv) > 1 else os.getenv("DOCS_ROOT", "data"))
# First CLI arg (passed by the Databricks job) overrides the docs root.

for folder, label in [("pos", 1), ("neg", 0)]:
    for file in (BASE / folder).glob("*.txt"):
        rows.append({
            "filename": file.name,
            "text": file.read_text(encoding="utf-8"),
            "label": label
        })

if not rows:
    raise SystemExit(f"No documents found under {BASE} - refusing to overwrite bronze.")

df = spark.createDataFrame(rows)

df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("workspace.bronze.webpages")

print(f"Ingested {len(rows)} documents.")