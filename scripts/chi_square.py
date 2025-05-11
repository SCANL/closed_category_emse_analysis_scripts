import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency, norm, chi2
import os

# === Load Unified TSV File ===
df = pd.read_csv("../data/Tagger Open Coding - Name and Grammar Pattern.tsv", sep='\t', dtype=str)

# === Strip and Prepare Columns ===
df['language'] = df['language'].str.strip()
df['context'] = df['context'].str.strip()
df['grammar pattern'] = df['grammar pattern'].fillna('').str.strip()

# === Closed-category Tags to Track ===
closed_tags = ["D", "DT", "P", "CJ"]

# === Initialize Count Structures ===
language_counts = {tag: {} for tag in closed_tags}
context_counts = {tag: {} for tag in closed_tags}
all_languages = set()
all_contexts = set()

# === Tally Closed Category Occurrences ===
for _, row in df.iterrows():
    grammar_tags = row['grammar pattern'].split()
    language = row['language']
    context = row['context']

    found_tags = set(grammar_tags) & set(closed_tags)
    
    for tag in found_tags:
        language_counts[tag][language] = language_counts[tag].get(language, 0) + 1
        context_counts[tag][context] = context_counts[tag].get(context, 0) + 1
        all_languages.add(language)
        all_contexts.add(context)

# === Create DataFrames ===
tag_language_table = pd.DataFrame(language_counts).fillna(0).astype(int).T
tag_language_table = tag_language_table.reindex(columns=sorted(all_languages))

tag_context_table = pd.DataFrame(context_counts).fillna(0).astype(int).T
tag_context_table = tag_context_table.reindex(columns=sorted(all_contexts))

# === Markdown Helper ===
def df_to_markdown(df, caption, bold_largest=True):
    markdown = f"### {caption}\n\n"
    headers = " | ".join([""] + list(df.columns)) + "\n"
    separators = "| " + " | ".join(["---"] * (len(df.columns) + 1)) + "\n"
    markdown += headers + separators
    for idx, row in df.iterrows():
        formatted = row.tolist()
        markdown += f"{idx} | " + " | ".join(map(str, formatted)) + "\n"
    return markdown + "\n"

# === Chi-square Analysis ===
def analyze_table(observed_table, output_prefix):
    chi2_stat, p_val, dof, expected = chi2_contingency(observed_table)
    chi2_critical = chi2.ppf(0.95, dof)
    chi2_components = (observed_table - expected) ** 2 / expected
    chi2_components["Chi-square per row"] = chi2_components.sum(axis=1)
    chi2_components.loc["Chi-square per column"] = chi2_components.sum()
    chi2_components.loc["Chi-square Sum"] = chi2_stat

    n = observed_table.values.sum()
    row_totals = observed_table.sum(axis=1).values.reshape(-1, 1)
    col_totals = observed_table.sum(axis=0).values.reshape(1, -1)
    std_error = np.sqrt(expected * (1 - row_totals / n) * (1 - col_totals / n))
    residuals = (observed_table - expected) / std_error
    residuals_df = pd.DataFrame(residuals, index=observed_table.index, columns=observed_table.columns)

    alpha = 0.05
    num_tests = observed_table.size
    critical_z = norm.ppf(1 - alpha / (2 * num_tests))

    residuals_marked = residuals_df.copy().round(6).astype(str)
    sig_mask = residuals_df.abs() >= critical_z
    residuals_marked[sig_mask] = residuals_df[sig_mask].round(6).astype(str) + " *"

    # === Save Output ===
    os.makedirs("../output", exist_ok=True)
    chi2_components.to_csv(f"../output/chi2_{output_prefix}.csv")
    residuals_marked.to_csv(f"../output/adjusted_residuals_{output_prefix}.csv")

    chi2_header = (
        f"Results of Pearson’s Chi Squared Test. df = {dof}, α = {alpha}, "
        f"critical value = {chi2_critical:.3f}, test statistic = {chi2_stat:.3f}\n\n"
    )
    bonferroni_alpha = alpha / num_tests
    bonferroni_header = (
        f"Adjusted Pearson’s Residuals Results. With Bonferroni Correction, a significant result is "
        f"α = {alpha:.2f}/{num_tests} = {bonferroni_alpha:.4f}, which translates to a ± {critical_z:.2f} critical value.\n\n"
    )

    chi2_md = chi2_header + df_to_markdown(chi2_components.round(6), f"Chi-Square Contributions: {output_prefix.replace('_', ' ').title()}")
    residuals_md = bonferroni_header + df_to_markdown(residuals_marked, f"Adjusted Pearson Residuals: {output_prefix.replace('_', ' ').title()}", bold_largest=False)

    with open(f"../output/markdown_{output_prefix}.md", "w") as f:
        f.write(chi2_md)
        f.write("\n")
        f.write(residuals_md)

# === Run Analysis ===
analyze_table(tag_language_table, "tag_language")
analyze_table(tag_context_table, "tag_context")
