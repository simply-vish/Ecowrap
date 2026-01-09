# recommend_alternatives_fixed.py
import pandas as pd
import numpy as np
import re
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

CSV_FILE = "combined_products_fixed_corrected.csv"

PRODUCT_COL = "product_name"
BARCODE_COL = "code"
CATEGORY_COL = "clean_category_fixed"
SCORE_COL = "biodegradability_score"
LABEL_COL = "biodegradability_label"

_token_re = re.compile(r"[a-z0-9]+")


def clean_code(val):
    """Convert float-like barcodes to pure string (no .0)."""
    try:
        s = str(val).strip()
        if s.endswith(".0"):
            s = s[:-2]
        return s
    except:
        return None


def tokens(text):
    if text is None:
        return []
    s = str(text).lower()
    return _token_re.findall(s)


def token_overlap(a, b):
    ta, tb = set(tokens(a)), set(tokens(b))
    if not ta or not tb:
        return 0
    return len(ta & tb) / max(1, min(len(ta), len(tb)))


class RecommenderFixed:
    def __init__(self, csv_path=CSV_FILE):
        self.df = pd.read_csv(csv_path)

        # clean barcode
        self.df[BARCODE_COL] = self.df[BARCODE_COL].apply(clean_code)

        # clean product names
        self.df[PRODUCT_COL] = (
            self.df[PRODUCT_COL]
            .astype(str)
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
        )
        self.df[PRODUCT_COL + "_lower"] = self.df[PRODUCT_COL].str.lower()

        # categories
        self.df[CATEGORY_COL] = (
            self.df[CATEGORY_COL].astype(str).fillna("").str.lower()
        )

        # numeric score
        self.df[SCORE_COL] = pd.to_numeric(
            self.df[SCORE_COL], errors="coerce"
        ).fillna(0.0)

        # for similarity search
        try:
            self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=2)
            self.tfidf = self.vectorizer.fit_transform(
                self.df[PRODUCT_COL + "_lower"]
            )
            self.tfidf_ok = True
        except:
            self.vectorizer = None
            self.tfidf = None
            self.tfidf_ok = False

    # ----------------------------
    # BARCODE LOOKUP
    # ----------------------------
    def find_by_code(self, code):
        c = clean_code(code)
        row = self.df[self.df[BARCODE_COL] == c]
        if not row.empty:
            return row.iloc[0]
        return None

    # ----------------------------
    # NAME LOOKUP
    # ----------------------------
    def find_by_name(self, query):
        q = str(query).lower().strip()

        exact = self.df[self.df[PRODUCT_COL + "_lower"] == q]
        if not exact.empty:
            return exact.iloc[0]

        fuzzy = difflib.get_close_matches(
            q, self.df[PRODUCT_COL + "_lower"].tolist(), n=1, cutoff=0.75
        )
        if fuzzy:
            return self.df[self.df[PRODUCT_COL + "_lower"] == fuzzy[0]].iloc[0]

        partial = self.df[self.df[PRODUCT_COL + "_lower"].str.contains(q)]
        if not partial.empty:
            return partial.iloc[0]

        return None

    # ----------------------------
    # RECOMMENDER
    # ----------------------------
    def recommend(self, name=None, code=None, top_k=5):
        # 1) If barcode provided → barcode search first
        row = None
        if code:
            row = self.find_by_code(code)
        if row is None and name:
            row = self.find_by_name(name)

        if row is None:
            return {"error": "Product not found"}

        pname = row[PRODUCT_COL]
        pcat = row[CATEGORY_COL]
        pscore = row[SCORE_COL]

        # Same category filtering
        candidates = self.df[self.df[CATEGORY_COL] == pcat]
        candidates = candidates[candidates[PRODUCT_COL] != pname]
        candidates = candidates[candidates[SCORE_COL] >= pscore]

        # Sort by score descending
        candidates = candidates.sort_values(SCORE_COL, ascending=False)

        recs = [
            {
                "product_name": r[PRODUCT_COL],
                "score": float(r[SCORE_COL]),
                "category": r[CATEGORY_COL],
            }
            for _, r in candidates.head(top_k).iterrows()
        ]

        return {
            "product": {
                "name": pname,
                "category": pcat,
                "score": pscore,
            },
            "recommendations": recs,
        }
