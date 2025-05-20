import os
import csv
from collections import Counter, defaultdict

# File paths
files = {
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

def summarize_records(name, records):
    print(f"\n{name} — Language Counts")
    lang_counts = count_by_column(records, "language", target_languages)
    for lang in sorted(target_languages):
        print(f"  {lang}: {lang_counts.get(lang, 0)}")

    total_terms = 0
    terms_per_language = Counter()
    identifiers_with_pos_tags = Counter()
    pos_counts_by_language = defaultdict(lambda: Counter())
    total_per_pos = Counter()

    for row in records:
        lang = row.get("language", "").strip()
        pattern = row.get("grammar pattern", "").strip().split()
        if not pattern:
            continue

        identifiers_with_pos_tags[lang] += 1
        for tag in pattern:
            terms_per_language[lang] += 1
            pos_counts_by_language[lang][tag] += 1
            total_per_pos[tag] += 1
            total_terms += 1

    print(f"\n{name} — Totals")
    print("  Total PoS-tagged terms:", total_terms)
    print("  Total identifiers with PoS tags per language:")
    for lang in sorted(target_languages):
        print(f"    {lang}: {identifiers_with_pos_tags[lang]}")
    print("  Total PoS-tagged terms per language:")
    for lang in sorted(target_languages):
        print(f"    {lang}: {terms_per_language[lang]}")

    print(f"\n{name} — Per-PoS breakdown by language:")
    for lang in sorted(target_languages):
        total_lang_terms = terms_per_language[lang]
        print(f"  {lang}:")
        for tag in sorted(pos_counts_by_language[lang]):
            count = pos_counts_by_language[lang][tag]
            pct = (count / total_lang_terms * 100) if total_lang_terms > 0 else 0
            print(f"    {tag}: {count} ({pct:.2f}%)")

    print(f"\n{name} — PoS totals across all languages:")
    sorted_total_pos = sorted(total_per_pos.items(), key=lambda x: x[1], reverse=True)
    for tag, count in sorted_total_pos:
        pct = (count / total_terms * 100) if total_terms > 0 else 0
        print(f"  {tag}: {count} ({pct:.2f}%)")

    print(f"\n{name} — PoS breakdown by context (all languages):")
    pos_counts_by_context = defaultdict(lambda: Counter())
    terms_per_context = Counter()

    for row in records:
        context = row.get("context", "").strip()
        pattern = row.get("grammar pattern", "").strip().split()
        for tag in pattern:
            pos_counts_by_context[context][tag] += 1
            terms_per_context[context] += 1

    for context in sorted(pos_counts_by_context):
        print(f"  Context: {context}")
        total = terms_per_context[context]
        sorted_tags = sorted(pos_counts_by_context[context].items(), key=lambda x: x[1], reverse=True)
        for tag, count in sorted_tags:
            pct = (count / total * 100) if total > 0 else 0
            print(f"    {tag}: {count} ({pct:.2f}%)")
    
    print(f"\n{name} — Identifier counts by context (all languages):")
    context_counter = Counter()

    for row in records:
        context = row.get("context", "").strip()
        if context:
            context_counter[context] += 1

    total_context_items = sum(context_counter.values())
    for context, count in context_counter.most_common():
        pct = (count / total_context_items * 100) if total_context_items > 0 else 0
        print(f"  {context}: {count} ({pct:.2f}%)")
    print(f"\n{name} — Most common grammar patterns per closed-category:")
    pattern_counter_per_category = defaultdict(Counter)

    for row in records:
        pattern = row.get("grammar pattern", "").strip()
        tags = pattern.split()
        if not tags:
            continue

        found_categories = set()
        for tag in tags:
            category = tag_to_category.get(tag)
            if category:
                found_categories.add(category)

        for category in found_categories:
            pattern_counter_per_category[category][pattern] += 1

    for category in sorted(pattern_counter_per_category):
        print(f"  {category}:")
        total = sum(pattern_counter_per_category[category].values())
        for pat, count in pattern_counter_per_category[category].most_common(15):
            pct = (count / total * 100) if total > 0 else 0
            print(f"    {pat}: {count} ({pct:.2f}%)")
# Run
print("\n=== FULL DATASET ===")
full_records = process_file(files["Full"])
summarize_records("Full", full_records)
