import os
from collections import Counter

# List of files to process
files = {
    "Digit": "../data/Digit Axial Code Annotations - digit_axial_code_dual_axis.tsv",
    "Conjunction": "../data/Conjunction Axial Code Annotations - conjunction_axial_codes_final.tsv",
    "Preposition": "../data/Preposition Axial Code Annotations - refined_axial_code_labels_updated.tsv",
    "Determiner": "../data/Determiner Axial Code Anntoations - determiner_axial_code_validation.tsv"
}

# Languages we care about
target_languages = {"C", "C++", "Java"}

# Function to count language appearances
def count_languages(file_path, target_langs):
    counts = Counter()
    with open(file_path, encoding="utf-8") as f:
        header = f.readline().strip().split("\t")
        if "language" not in header:
            return {lang: 0 for lang in target_langs}
        lang_idx = header.index("language")
        for line in f:
            columns = line.strip().split("\t")
            if len(columns) > lang_idx:
                lang = columns[lang_idx]
                if lang in target_langs:
                    counts[lang] += 1
    return {lang: counts.get(lang, 0) for lang in target_langs}

# Count languages for each file
all_counts = {}
total_counts = Counter()
for name, filename in files.items():
    if os.path.exists(filename):
        file_counts = count_languages(filename, target_languages)
        all_counts[name] = file_counts
        for lang, count in file_counts.items():
            total_counts[lang] += count
    else:
        print(f"Warning: File not found: {filename}")
        all_counts[name] = {lang: 0 for lang in target_languages}

# Print results
print(f"{'File':<15} {'C':>5} {'C++':>5} {'Java':>5}")
for name, counts in all_counts.items():
    print(f"{name:<15} {counts['C']:>5} {counts['C++']:>5} {counts['Java']:>5}")

# Print total sums
print("-" * 34)
print(f"{'TOTAL':<15} {total_counts['C']:>5} {total_counts['C++']:>5} {total_counts['Java']:>5}")