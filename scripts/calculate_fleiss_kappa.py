import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from statsmodels.stats.inter_rater import fleiss_kappa

def prepare_fleiss_matrix_single_axis(df, annotator_columns):
    """
    Prepare data matrix for Fleiss' Kappa from single-axis annotation columns.
    """
    all_annotations = []
    for col in annotator_columns:
        all_annotations.extend(df[col].dropna().tolist())

    label_encoder = LabelEncoder()
    label_encoder.fit(all_annotations)
    n_categories = len(label_encoder.classes_)

    matrix = []
    for _, row in df.iterrows():
        counts = np.zeros(n_categories)
        for col in annotator_columns:
            label = row[col]
            if pd.notna(label):
                index = label_encoder.transform([label])[0]
                counts[index] += 1
        matrix.append(counts)
    return np.array(matrix)

def prepare_fleiss_matrix_composite_labels(df, annotator_pairs):
    """
    Prepare data matrix for Fleiss' Kappa from dual-axis annotation columns
    using composite Role::Meaning labels.
    """
    all_composites = []
    for role_col, meaning_col in annotator_pairs:
        combined = df[role_col].fillna('') + "::" + df[meaning_col].fillna('')
        all_composites.extend(combined.tolist())

    label_encoder = LabelEncoder()
    label_encoder.fit(all_composites)
    n_categories = len(label_encoder.classes_)

    matrix = []
    for _, row in df.iterrows():
        counts = np.zeros(n_categories)
        for role_col, meaning_col in annotator_pairs:
            label = f"{row[role_col]}::{row[meaning_col]}"
            if "::" in label and label != "::":
                index = label_encoder.transform([label])[0]
                counts[index] += 1
        matrix.append(counts)
    return np.array(matrix)

def calculate_fleiss_kappa_single(file_path, sep="\t"):
    df = pd.read_csv(file_path, sep=sep)
    annotator_cols = [col for col in df.columns if "Axial Code" in col]
    matrix = prepare_fleiss_matrix_single_axis(df, annotator_cols)
    return fleiss_kappa(matrix)

def calculate_fleiss_kappa_dual(file_path, sep="\t"):
    df = pd.read_csv(file_path, sep=sep)
    annotator_pairs = [
        ("Christian Axial Code Role", "Christian Axial Code Meaning"),
        ("Syreen Axial Code Role", "Syreen Axial Code Meaning"),
        ("Anthony Axial Code Role", "Anthony Axial Code Meaning"),
    ]
    matrix = prepare_fleiss_matrix_composite_labels(df, annotator_pairs)
    return fleiss_kappa(matrix)

# Example usage:
if __name__ == "__main__":
    digit_file = "../data/Digit Axial Code Annotations - digit_axial_code_dual_axis.tsv"
    determiner_file = "../data/Determiner Axial Code Anntoations - determiner_axial_code_validation.tsv"
    preposition_file = "../data/Preposition Axial Code Annotations - refined_axial_code_labels_updated.tsv"
    conjunction_file = "../data/Conjunction Axial Code Annotations - conjunction_axial_codes_final.tsv"

    print("Digit (dual-axis) Fleiss' Kappa:", calculate_fleiss_kappa_dual(digit_file))
    print("Determiner (single-axis) Fleiss' Kappa:", calculate_fleiss_kappa_single(determiner_file))
    print("Preposition (single-axis) Fleiss' Kappa:", calculate_fleiss_kappa_single(preposition_file))
    print("Conjunction (single-axis) Fleiss' Kappa:", calculate_fleiss_kappa_single(conjunction_file))
