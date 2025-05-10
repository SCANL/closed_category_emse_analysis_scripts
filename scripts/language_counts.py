import os
import csv
from collections import Counter, defaultdict

# File paths
files = {
    "Digit": "../data/Statistical Analysis - D.tsv",
    "Conjunction": "../data/Statistical Analysis - CJ.tsv",
    "Preposition": "../data/Statistical Analysis - P.tsv",
    "Determiner": "../data/Statistical Analysis - DT.tsv",
    "Full": "../data/Tagger Open Coding - Name and Grammar Pattern.tsv",
}

# Target categories and languages
target_languages = {"C", "C++", "Java"}
tag_to_category = {"DT": "Determiner", "D": "Digit", "P": "Preposition", "CJ": "Conjunction"}

# Helpers
def process_file(file_path):
    with open(file_path, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        return list(reader)

def count_by_column(records, column, valid_values):
    counter = Counter()
    for row in records:
        val = row.get(column, "").strip()
        if val in valid_values:
            counter[val] += 1
    return counter

def top_closed_category_words(records):
    word_counter = defaultdict(Counter)
    for row in records:
        split = row.get("split", "").strip().split()
        pattern = row.get("grammar pattern", "").strip().split()
        if len(split) != len(pattern):
            continue
        for word, tag in zip(split, pattern):
            category = tag_to_category.get(tag)
            if category:
                word_counter[category][word] += 1
    return word_counter

# === Process and Aggregate ===
def summarize_records(name, records):
    print(f"\n{name} — Language Counts")
    lang_counts = count_by_column(records, "language", target_languages)
    for lang in sorted(target_languages):
        print(f"  {lang}: {lang_counts.get(lang, 0)}")

    print(f"{name} — Context Counts")
    ctx_counts = count_by_column(records, "context", set())
    for ctx, count in ctx_counts.most_common():
        print(f"  {ctx}: {count}")

    print(f"{name} — Top Closed Category Words")
    word_counts = top_closed_category_words(records)
    for category, counter in word_counts.items():
        print(f"  {category}:")
        for word, count in counter.most_common(10):
            print(f"    {word}: {count}")

# Run for closed-category files
for name, path in files.items():
    if not os.path.exists(path):
        print(f"Missing file: {name}")
        continue
    records = process_file(path)
    if name != "Full":
        summarize_records(name, records)

# Separate handling for full file
print("\n=== FULL DATASET ===")
full_records = process_file(files["Full"])
summarize_records("Full", full_records)
