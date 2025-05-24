# Closed-Category Grammar Pattern Analysis

This repository contains scripts and data used in our study of closed-category grammar patterns in source code identifiers. We analyze how determiners, conjunctions, prepositions, and digits encode behavior-relevant semantics across programming languages, program contexts, and software domains.

## Repository Structure

### `scripts/`

Contains all analysis and data-processing scripts:

- **`calculate_fleiss_kappa.py`**  
  Computes Fleiss’ Kappa for inter-annotator agreement across axial and grammar pattern codes.

- **`chi_square.py`**  
  Performs chi-squared tests on grammar pattern distributions across programming languages and structural contexts (RQ1).

- **`dataset_stats_summary.py`**  
  Generates descriptive statistics on:
  - Closed-category usage per part of speech, language, and context.
  - Totals across identifiers and projects.

- **`system_analysis_mann_whitney.py`**  
  Runs Mann-Whitney U tests to compare closed-category usage in domain-specific vs. general-purpose software (RQ2).

- **`update_markdown_with_counts.py`**  
  Fills category-specific Markdown templates with grammar pattern frequency data extracted from the annotation TSVs.

---

### `data/`

#### Annotation Files
- **Per-category axial code TSVs**  
  (e.g., `conjunction_axial_codes_final.tsv`, `digit_axial_code_dual_axis.tsv`)  
  Contain open and axial codes for identifiers tagged with that part of speech.

- **Global annotation**  
  - `Tagger Open Coding - Name and Grammar Pattern.tsv`  
    Grammar pattern data for all identifiers, across all categories.

- **Domain metadata**  
  - `domain_specific_systems_for_rq2.tsv`  
    Identifies which systems are considered domain-specific for RQ2.

#### Markdown Templates
- `.md` files such as `Determiner_Selective_Code_Summary.md`  
  These are auto-filled by `update_markdown_with_counts.py`.

#### Statistical Input
- Normalized usage stats by system:
  - `word_system_stats_with_sloc_domain.csv`
  - `word_system_stats_with_sloc_general.csv`

---

## Usage

To run any script:

1. Open a terminal in the root of the repository.
2. Navigate to the `scripts/` directory:
   ```bash
   cd scripts/
   ```
3. Execute the desired script:
    python calculate_fleiss_kappa.py
    python chi_square.py
    python dataset_stats_summary.py
    python system_analysis_mann_whitney.py
    python update_markdown_with_counts.py
