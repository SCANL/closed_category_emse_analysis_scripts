import pandas as pd
from collections import Counter

files = {
    "DT": "../data/Statistical Analysis - DT.tsv",  # Determiner
    "CJ": "../data/Statistical Analysis - CJ.tsv",  # Conjunction
    "D": "../data/Statistical Analysis - D.tsv",     # Digit
    "P": "../data/Statistical Analysis - P.tsv",     # Preposition
}

# Closed-category PoS tags to look for in each file
closed_category_tags = {
    "DT": {"DT"},
    "CJ": {"CJ"},
    "D": {"D"},
    "P": {"P"},
}

# Store results
top_terms_by_category = {}

for category, filepath in files.items():
    df = pd.read_csv(filepath, sep="\t")

    closed_terms = []

    for _, row in df.iterrows():
        split_words = row["split"].split(" ")
        grammar_tags = row["grammar pattern"].split(" ")

        # Match words with grammar tags by position
        for word, tag in zip(split_words, grammar_tags):
            if tag in closed_category_tags[category]:
                closed_terms.append(word)

    # Count frequencies
    counter = Counter(closed_terms)
    total = sum(counter.values())

    # Get top 5 terms
    top5 = counter.most_common(5)

    top_terms_by_category[category] = [(term, freq, f"{(freq / total) * 100:.2f}%") for term, freq in top5]

# Prepare Markdown Table
categories = ["DT", "CJ", "D", "P"]
header = "| Rank | " + " | ".join(categories) + " |"
separator = "|------" + "|------" * len(categories) + "|"

rows = []
for i in range(5):
    row = [f"{i + 1}"]
    for cat in categories:
        if i < len(top_terms_by_category.get(cat, [])):
            term, freq, percent = top_terms_by_category[cat][i]
            cell = f"{term} ({freq}, {percent})"
        else:
            cell = "-"
        row.append(cell)
    rows.append("| " + " | ".join(row) + " |")

markdown_table = "\n".join([header, separator] + rows)

print("\nMarkdown Table of Top 5 Closed-Category Terms:\n")
print(markdown_table)
