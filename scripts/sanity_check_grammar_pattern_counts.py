import sys
import csv
from collections import Counter

def count_grammar_patterns(file_path):
    pattern_counter = Counter()

    with open(file_path, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            pattern = row.get("grammar pattern", "").strip()
            if pattern:
                pattern_counter[pattern] += 1

    return pattern_counter

def main():
    if len(sys.argv) != 2:
        print("Usage: python grammar_pattern_counter.py <file.tsv>")
        sys.exit(1)

    file_path = sys.argv[1]
    pattern_counter = count_grammar_patterns(file_path)

    print("Grammar Pattern Frequencies:")
    for pattern, count in pattern_counter.most_common():
        print(f"{pattern}: {count}")

if __name__ == "__main__":
    main()