

def print_closed_category_context_breakdown(name, records):
    print(f"\n{name} — Closed Category Breakdown by Context:")
    category_context_counts = defaultdict(lambda: Counter())
    context_totals = Counter()
    category_totals = Counter()

    for row in records:
        context = row.get("context", "").strip()
        pattern = row.get("grammar pattern", "").strip().split()
        found_categories = set()
        for tag in pattern:
            category = tag_to_category.get(tag)
            if category:
                found_categories.add(category)
        for category in found_categories:
            category_context_counts[category][context] += 1
            context_totals[context] += 1
            category_totals[category] += 1

    for category in sorted(category_context_counts):
        print(f"  {category}:")
        for context, count in category_context_counts[category].most_common():
            context_total = context_totals[context]
            category_total = category_totals[category]
            pct_context = (count / context_total * 100) if context_total > 0 else 0
            pct_category = (count / category_total * 100) if category_total > 0 else 0
            print(f"    {context}: {count} ({pct_context:.2f}% of context out of {context_total}, {pct_category:.2f}% of {category} out of {category_total})")
def count_closed_category_words(records):
    word_counter = defaultdict(Counter)
    for row in records:
        split = row.get("split", "").strip().split()
        pattern = row.get("grammar pattern", "").strip().split()
        if len(split) != len(pattern):
            continue
        for word, tag in zip(split, pattern):
            category = tag_to_category.get(tag)
            if category:
                word_counter[category][word.lower()] += 1
    return word_counter

def print_closed_category_word_summary(name, records):
    print(f"\n{name} — Top Closed Category Words:")
    word_counter = count_closed_category_words(records)
    for category in sorted(word_counter):
        print(f"  {category}:")
        total = sum(word_counter[category].values())
        for word, count in word_counter[category].most_common(10):
            pct = (count / total * 100) if total > 0 else 0
            print(f"    {word}: {count} ({pct:.2f}%)")

def print_closed_category_identifier_summary(name, records):
    print(f"\n{name} — Identifier Counts by Closed Category:")
    total_identifiers = len(records)
    category_identifier_counts = defaultdict(int)
    for row in records:
        pattern = row.get("grammar pattern", "").strip().split()
        found_categories = set()
        for tag in pattern:
            category = tag_to_category.get(tag)
            if category:
                found_categories.add(category)
        for category in found_categories:
            category_identifier_counts[category] += 1
    print(f"  Total identifiers: {total_identifiers}")
    for category, count in category_identifier_counts.items():
        print(f"  {category}: {count} ({(count/total_identifiers)*100:.2f}%)")

import os
import csv
from collections import Counter, defaultdict

# File paths
files = {
    "Full": "../data/Tagger Open Coding - Name and Grammar Pattern.tsv",
    "Determiner": "../data/Determiner Axial Code Anntoations - determiner_axial_code_validation.tsv",
    "Digit": "../data/Digit Axial Code Annotations - digit_axial_code_dual_axis.tsv",
    "Preposition": "../data/Preposition Axial Code Annotations - refined_axial_code_labels_updated.tsv",
    "Conjunction": "../data/Conjunction Axial Code Annotations - conjunction_axial_codes_final.tsv",
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
            print(f"    {tag}: {count} ({pct:.2f}%) out of {total_lang_terms}")

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
            print(f"    {tag}: {count} ({pct:.2f}%) out of {total}")
    
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

# Global Report
print("\n=== GLOBAL REPORT ===")
full_records = process_file(files["Full"])
summarize_records("Global", full_records)
print_closed_category_identifier_summary("Global", full_records)
print_closed_category_context_breakdown("Global", full_records)
print_closed_category_word_summary("Global", full_records)

# Per-Closed-Category Reports
print("\n=== PER-CLOSED-CATEGORY REPORTS ===")
for category in ["Determiner", "Digit", "Preposition", "Conjunction"]:
    print(f"\n--- {category.upper()} REPORT ---")
    records = process_file(files[category])
    summarize_records(category, records)
    print_closed_category_identifier_summary(category, records)
    print_closed_category_word_summary(category, records)
