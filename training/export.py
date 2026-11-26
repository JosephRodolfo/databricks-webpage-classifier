"""Export the trained pipeline to model.json for the browser extension.

The JSON schema must match what
`terms-and-conditions-extension/src/scorer.ts` expects:

    params     - TF-IDF settings (lowercase, strip_accents, token_pattern,
                 ngram_range, use_idf, smooth_idf, sublinear_tf, norm)
    vocab      - token -> column index (ints)
    idf        - list of floats aligned to column index
    coef       - list of floats aligned to column index
    intercept  - float
    threshold  - float (probability cutoff for "is terms")

Run after training:

    python -m training.train
    python -m training.export
"""

import json
import pathlib

import joblib

MODEL_PATH = pathlib.Path("models/model.joblib")
OUTPUT_PATH = pathlib.Path("models/model.json")
THRESHOLD = 0.80


def main() -> None:
    pipe = joblib.load(MODEL_PATH)

    # Positional access keeps this independent of step names.
    vec, clf = pipe[0], pipe[-1]
    p = vec.get_params()

    # `strip_accents` is typed `"unicode" | false` in scorer.ts, so map
    # None -> False to stay type-correct while behaving identically.
    strip_accents = p["strip_accents"] if p["strip_accents"] else False

    export = {
        "params": {
            "lowercase": bool(p["lowercase"]),
            "strip_accents": strip_accents,
            "token_pattern": p["token_pattern"],
            "ngram_range": [int(p["ngram_range"][0]), int(p["ngram_range"][1])],
            "use_idf": bool(p["use_idf"]),
            "smooth_idf": bool(p["smooth_idf"]),
            "sublinear_tf": bool(p["sublinear_tf"]),
            "norm": p["norm"],
        },
        # token -> column index (ints)
        "vocab": {str(tok): int(idx) for tok, idx in vec.vocabulary_.items()},
        "idf": [float(x) for x in vec.idf_],
        # classes_ is [0, 1]; row 0 is the coefficient vector for class 1 (pos).
        "coef": [float(x) for x in clf.coef_[0]],
        "intercept": float(clf.intercept_[0]),
        "threshold": THRESHOLD,
    }

    n_features = len(export["vocab"])
    assert len(export["idf"]) == n_features, "idf/vocab length mismatch"
    assert len(export["coef"]) == n_features, "coef/vocab length mismatch"

    OUTPUT_PATH.write_text(json.dumps(export, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH} ({n_features} features, threshold={THRESHOLD})")


if __name__ == "__main__":
    main()
