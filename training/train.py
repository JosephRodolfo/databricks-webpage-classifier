from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline

from connection import get_spark

spark = get_spark()

df = spark.table("workspace.gold.training_data").toPandas()

X_train, X_test, y_train, y_test = train_test_split(
    df["text"],
    df["label"],
    test_size=0.25,
    random_state=42,
    stratify=df["label"],
)

# Hyperparameters kept identical to the original browser-extension model
# so the exported JSON stays compatible with the extension's scorer.ts.
vec = TfidfVectorizer(
    lowercase=True,
    strip_accents="unicode",
    token_pattern=r"(?u)\b\w\w+\b",
    ngram_range=(1, 2),      # unigrams + bigrams
    min_df=2,                # drop ultra-rare terms
    max_features=12000,
    use_idf=True,
    smooth_idf=True,
    sublinear_tf=False,
    norm="l2",
)
clf = LogisticRegression(max_iter=300)
pipe = make_pipeline(vec, clf)

pipe.fit(X_train, y_train)

predictions = pipe.predict(X_test)

print(classification_report(y_test, predictions, digits=3))

Path("models").mkdir(exist_ok=True)
joblib.dump(pipe, "models/model.joblib")
print("Wrote models/model.joblib")