
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import mannwhitneyu
from statsmodels.stats.multitest import multipletests

# Load the CSV files
domain_raw = pd.read_csv('../data/word_system_stats_with_sloc_domain.csv')
general_raw = pd.read_csv('../data/word_system_stats_with_sloc_general.csv')

# --- Cleaning steps ---

def remove_digits(df):
    return df[~df['word'].str.isdigit()]

def remove_outliers(df):
    mean = df['normalized_system_count'].mean()
    std = df['normalized_system_count'].std()
    lower_bound = mean - 3 * std
    upper_bound = mean + 3 * std
    return df[(df['normalized_system_count'] >= lower_bound) & (df['normalized_system_count'] <= upper_bound)]

def filter_words_by_system_coverage(df, threshold):
    total_systems = df['system'].nunique()
    word_system_counts = df.groupby('word')['system'].nunique()
    eligible_words = word_system_counts[word_system_counts >= (total_systems * threshold)].index
    return df[df['word'].isin(eligible_words)]

def safe_log_transform(df):
    df = df.copy()
    df['log_normalized_system_count'] = np.log10(df['normalized_system_count'] + 1e-8)
    return df

def cliffs_delta(x, y):
    n_x = len(x)
    n_y = len(y)
    all_comparisons = [(int(xi > yi)) - (int(xi < yi)) for xi in x for yi in y]
    delta = np.sum(all_comparisons) / (n_x * n_y)
    return delta

# --- Run analysis for multiple thresholds ---

thresholds = np.arange(0.0, 1.1, 0.1)
global_summary_results = []
per_category_all_results = []

for threshold in thresholds:
    threshold = round(threshold, 2)
    print(f"\n=== Threshold: {threshold:.2f} ===")

    domain_df = remove_outliers(domain_raw)
    general_df = remove_outliers(general_raw)

    domain_df = filter_words_by_system_coverage(domain_df, threshold)
    general_df = filter_words_by_system_coverage(general_df, threshold)

    domain_df = safe_log_transform(domain_df)
    general_df = safe_log_transform(general_df)

    if domain_df.empty or general_df.empty:
        print("Skipped due to empty dataset after filtering.")
        continue

    stat, p_value = mannwhitneyu(
        domain_df['log_normalized_system_count'],
        general_df['log_normalized_system_count'],
        alternative='greater'
    )

    global_summary_results.append({
        'threshold': threshold,
        'domain_count': len(domain_df),
        'general_count': len(general_df),
        'domain_mean': domain_df['log_normalized_system_count'].mean(),
        'general_mean': general_df['log_normalized_system_count'].mean(),
        'domain_median': domain_df['log_normalized_system_count'].median(),
        'general_median': general_df['log_normalized_system_count'].median(),
        'statistic': stat,
        'p_value': p_value
    })

    # --- Per-Category Analysis ---
    categories_to_check = ['preposition', 'determiner', 'conjunction', 'digit']

    for category in categories_to_check:
        domain_subset = domain_df[domain_df['categories'].str.contains(category, na=False)]
        general_subset = general_df[general_df['categories'].str.contains(category, na=False)]

        if len(domain_subset) == 0 or len(general_subset) == 0:
            continue

        stat_cat, p_value_cat = mannwhitneyu(
            domain_subset['log_normalized_system_count'],
            general_subset['log_normalized_system_count'],
            alternative='greater'
        )

        delta = cliffs_delta(
            domain_subset['log_normalized_system_count'].values,
            general_subset['log_normalized_system_count'].values
        )

        per_category_all_results.append({
            'threshold': threshold,
            'category': category,
            'domain_count': len(domain_subset),
            'general_count': len(general_subset),
            'domain_mean': domain_subset['log_normalized_system_count'].mean(),
            'general_mean': general_subset['log_normalized_system_count'].mean(),
            'domain_median': domain_subset['log_normalized_system_count'].median(),
            'general_median': general_subset['log_normalized_system_count'].median(),
            'statistic': stat_cat,
            'p_value': p_value_cat,
            'cliffs_delta': delta,
            'low_sample_warning': (len(domain_subset) < 20 or len(general_subset) < 20)
        })

# Save all threshold global results
global_summary_df = pd.DataFrame(global_summary_results)
global_summary_df['fdr_corrected_p'] = multipletests(global_summary_df['p_value'], method='fdr_bh')[1]
global_summary_df['neg_log10_p'] = -np.log10(global_summary_df['p_value'])
global_summary_df.to_csv('../output/threshold_mannwhitney_summary_fdr.csv', index=False)

# Save all per-category results
per_category_df = pd.DataFrame(per_category_all_results)
per_category_df['fdr_corrected_p'] = multipletests(per_category_df['p_value'], method='fdr_bh')[1]
per_category_df['neg_log10_p'] = -np.log10(per_category_df['p_value'])
per_category_df.to_csv('../output/per_category_mannwhitney_summary_fdr.csv', index=False)

# --- Plot global p-values ---
plt.figure(figsize=(10, 6))
sns.lineplot(data=global_summary_df, x='threshold', y='neg_log10_p', marker='o', color='black', label='All Categories')
plt.axhline(-np.log10(0.05), color='red', linestyle='--', label='p = 0.05')
plt.title('Significance of Closed-Category Term Usage Across Thresholds')
plt.xlabel('Minimum Support Threshold (Proportion of Systems)')
plt.ylabel('-log10(p-value)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('../output/threshold_significance_global.png')
plt.close()

# --- Plot per-category p-values ---
plt.figure(figsize=(12, 6))
sns.lineplot(data=per_category_df, x='threshold', y='neg_log10_p', hue='category', marker='o')
plt.axhline(-np.log10(0.05), color='red', linestyle='--', label='p = 0.05')
plt.title('Significance of Closed-Category Term Usage by Category Across Thresholds')
plt.xlabel('Minimum Support Threshold (Proportion of Systems)')
plt.ylabel('-log10(p-value)')
plt.legend(title='Closed-Category')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('../output/threshold_significance_per_category.png')
plt.close()

print("\nSaved global and per-category results with FDR correction and low-sample warnings.")


# --- Plot Cliff's Delta per category ---
plt.figure(figsize=(12, 6))
sns.lineplot(data=per_category_df, x='threshold', y='cliffs_delta', hue='category', marker='o')

# Add interpretation bands
plt.axhspan(-0.147, 0.147, color='gray', alpha=0.1, label='negligible')
plt.axhspan(0.147, 0.33, color='yellow', alpha=0.1, label='small')
plt.axhspan(0.33, 0.474, color='orange', alpha=0.1, label='medium')
plt.axhspan(0.474, 1.0, color='red', alpha=0.1, label='large')
plt.axhspan(-0.33, -0.147, color='yellow', alpha=0.1)
plt.axhspan(-0.474, -0.33, color='orange', alpha=0.1)
plt.axhspan(-1.0, -0.474, color='red', alpha=0.1)

plt.title("Cliff's Delta per Category Across Thresholds")
plt.xlabel('Minimum Support Threshold (Proportion of Systems)')
plt.ylabel("Cliff's Delta")
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(title='Closed-Category')
plt.tight_layout()
plt.savefig('../output/cliffs_delta_per_category.png')
plt.close()
