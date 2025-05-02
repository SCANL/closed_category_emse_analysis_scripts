import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import mannwhitneyu

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

    domain_sorted = domain_df.sort_values(by='log_normalized_system_count', ascending=False)
    general_sorted = general_df.sort_values(by='log_normalized_system_count', ascending=False)

    stat, p_value = mannwhitneyu(
        domain_sorted['log_normalized_system_count'],
        general_sorted['log_normalized_system_count'],
        alternative='greater'
    )

    print(f"Mann-Whitney U Test Statistic: {stat:.2f}")
    print(f"p-value: {p_value:.6e}")

    global_summary_results.append({
        'threshold': threshold,
        'domain_count': len(domain_sorted),
        'general_count': len(general_sorted),
        'domain_mean': domain_sorted['log_normalized_system_count'].mean(),
        'general_mean': general_sorted['log_normalized_system_count'].mean(),
        'domain_median': domain_sorted['log_normalized_system_count'].median(),
        'general_median': general_sorted['log_normalized_system_count'].median(),
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
            'cliffs_delta': delta
        })

# Save all threshold global results
global_summary_df = pd.DataFrame(global_summary_results)
global_summary_df['neg_log10_p'] = -np.log10(global_summary_df['p_value'])
global_summary_df.to_csv('../output/threshold_mannwhitney_summary.csv', index=False)

# Save all per-category results
per_category_df = pd.DataFrame(per_category_all_results)
per_category_df['neg_log10_p'] = -np.log10(per_category_df['p_value'])
per_category_df.to_csv('../output/per_category_mannwhitney_summary.csv', index=False)

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

print("\nSaved global and per-category plots to output directory.")
