import pandas as pd

SCORING_TAGS = {
    "ukraine":          5,
    "cultural":         4,
    "heritage":         4,
    "preservation":     4,
    "arts":             3,
    "museum":           3,
    "displacement":     3,
    "refugee":          3,
    "human rights":     3,
    "eastern europe":   3,
    "war":              3,
    "conflict":         3,
    "youth":            2,
    "activism":         2,
    "digital":          2,
    "identity":         2,
    "community":        1,
}

def score_grant(text):
    if not text:
        return 0, []
    text_lower = text.lower()
    score = 0
    matched = []
    for tag, points in SCORING_TAGS.items():
        if tag in text_lower:
            score += points
            matched.append(tag)
    return score, matched

def filter_dataframe(df, text_columns, min_score=3):
    scores = []
    tags = []
    for _, row in df.iterrows():
        combined = " ".join(str(row.get(col, "")) for col in text_columns)
        s, t = score_grant(combined)
        scores.append(s)
        tags.append(", ".join(t))
    df = df.copy()
    df["relevance_score"] = scores
    df["matched_tags"] = tags
    return df[df["relevance_score"] >= min_score].sort_values(
        "relevance_score", ascending=False
    )

try:
    grants = pd.read_csv("grants_gov_raw.csv")
    filtered_grants = filter_dataframe(
        grants,
        text_columns=["program", "description", "funder"],
        min_score=3
    )
    filtered_grants.to_csv("filtered_grants.csv", index=False)
    print(f"Filtered to {len(filtered_grants)} relevant grants")
except FileNotFoundError:
    print("grants_gov_raw.csv not found — skipping")

try:
    foundations = pd.read_csv("foundations_raw.csv")
    filtered_foundations = filter_dataframe(
        foundations,
        text_columns=["funder", "ntee_code"],
        min_score=1
    )
    filtered_foundations.to_csv("filtered_foundations.csv", index=False)
    print(f"Filtered to {len(filtered_foundations)} relevant foundations")
except FileNotFoundError:
    print("foundations_raw.csv not found — skipping")
