import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency, norm, chi2
import os

# === Define Input Files ===
files = {
    "D": "../data/Statistical Analysis - D.tsv",
    "CJ": "../data/Statistical Analysis - CJ.tsv",
    "P": "../data/Statistical Analysis - P.tsv",
    "DT": "../data/Statistical Analysis - DT.tsv"
}

# === Initialize Language and Context Counters ===
language_counts = {}
context_counts = {}

all_languages = set()
all_contexts = set()

# === Read and Aggregate Counts ===
for tag, filepath in files.items():
    df = pd.read_csv(filepath, sep='\t', dtype=str)
    df['language'] = df['language'].str.strip()
    df['context'] = df['context'].str.strip()

    lang_count = df['language'].value_counts().to_dict()
    ctx_count = df['context'].value_counts().to_dict()

    for lang, count in lang_count.items():
        all_languages.add(lang)
        language_counts.setdefault(tag, {}).setdefault(lang, 0)
        language_counts[tag][lang] += count

    for ctx, count in ctx_count.items():
        all_contexts.add(ctx)
        context_counts.setdefault(tag, {}).setdefault(ctx, 0)
        context_counts[tag][ctx] += count

# === Create Tables ===
tag_language_table = pd.DataFrame(language_counts).fillna(0).astype(int).T
tag_language_table = tag_language_table.reindex(columns=sorted(all_languages))

tag_context_table = pd.DataFrame(context_counts).fillna(0).astype(int).T
tag_context_table = tag_context_table.reindex(columns=sorted(all_contexts))

# === Helper to Convert to Markdown ===
def df_to_markdown(df, caption, bold_largest=True):
    markdown = f"### {caption}\n\n"
    headers = " | ".join([""] + list(df.columns)) + "\n"
    separators = "| " + " | ".join(["---"] * (len(df.columns) + 1)) + "\n"
    markdown += headers + separators

    for idx, row in df.iterrows():
        if bold_largest and row.dtype == "float64":
            max_val = row.max()
            formatted = [f"**{v:.6f}**" if v == max_val else f"{v:.6f}" for v in row]
        else:
            formatted = row.tolist()
        markdown += f"{idx} | " + " | ".join(map(str, formatted)) + "\n"
    return markdown + "\n"

# === Function to Run Chi-Square, Residuals, and Bonferroni ===
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

    # === Save CSVs ===
    os.makedirs("../output", exist_ok=True)
    chi2_components.to_csv(f"../output/chi2_{output_prefix}.csv")
    residuals_marked.to_csv(f"../output/adjusted_residuals_{output_prefix}.csv")

    # === Save Markdown with explanatory headers ===
    chi2_header = (
        f"Results of Pearson’s Chi Squared Test. df = {dof}, α = {alpha}, "
        f"critical value = {chi2_critical:.3f}, test statistic = {chi2_stat:.3f}\n\n"
    )
    bonferroni_alpha = alpha / num_tests
    bonferroni_header = (
        f"Adjusted Pearson’s Residuals Results. With Bonferroni Correction, a significant result is "
        f"α = {alpha:.2f}/{num_tests} = {bonferroni_alpha:.4f}, which translates to a ± {critical_z:.2f} critical value.\n\n"
    )

    chi2_markdown = chi2_header + df_to_markdown(chi2_components.round(6), f"Chi-Square Contributions: {output_prefix.replace('_', ' ').title()}")
    residuals_markdown = bonferroni_header + df_to_markdown(residuals_marked, f"Adjusted Pearson Residuals: {output_prefix.replace('_', ' ').title()}", bold_largest=False)

    with open(f"../output/markdown_{output_prefix}.md", "w") as f:
        f.write(chi2_markdown)
        f.write("\n")
        f.write(residuals_markdown)

# === Run Analyses ===
analyze_table(tag_language_table, "tag_language")
analyze_table(tag_context_table, "tag_context")