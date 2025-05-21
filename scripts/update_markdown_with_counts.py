
import pandas as pd
import re
from collections import Counter, defaultdict
from pathlib import Path

# === Load & Prepare Data ===

def summarize_counts_fixed(df, group_col, context_col='context', grammar_col='grammar pattern', lang_col='language'):
    summary = defaultdict(lambda: {'Contexts': Counter(), 'Grammar patterns': Counter(), 'Language': Counter()})
    for _, row in df.iterrows():
        key = row[group_col]
        summary[key]['Contexts'][str(row[context_col]).strip()] += 1
        summary[key]['Grammar patterns'][str(row[grammar_col]).strip()] += 1
        summary[key]['Language'][str(row[lang_col]).strip()] += 1
    return summary

def compute_language_counts(*dfs, lang_col='language'):
    combined_counts = Counter()
    for df in dfs:
        combined_counts.update(df[lang_col].str.strip().str.upper().value_counts().to_dict())
    return dict(combined_counts)

# === Format Markdown Summary for Each Axial Code ===

def format_summary_block(summary_data, language_counts):
    def format_counter(counter, label):
        if label == "Language":
            parts = []
            for lang, count in counter.items():
                lang_upper = lang.upper()
                total = language_counts.get(lang_upper, None)
                if total:
                    norm = round(count / total, 2)
                    parts.append(f"{lang_upper} ({count}, {norm*100:.0f}%)")
                else:
                    parts.append(f"{lang_upper} ({count})")
            return f"**{label}:** " + ", ".join(parts)
        else:
            return f"**{label}:** " + ", ".join(f"{k.title()} ({v})" for k, v in counter.items())

    contexts_line = format_counter(summary_data["Contexts"], "Contexts")
    grammar_line = format_counter(summary_data["Grammar patterns"], "Grammar patterns")
    language_line = format_counter(summary_data["Language"], "Language")

    return f"{contexts_line}\n{grammar_line}\n{language_line}\n"

# === Patch Markdown Content ===

def patch_markdown(md_text, summary_dict, code_keys, language_counts):
    code_pattern = re.compile(r"^#+\s(.+?)\s\((\d+) items\)", re.MULTILINE)
    last_end = 0
    new_lines = []
    
    for match in code_pattern.finditer(md_text):
        code_title = match.group(1).strip()
        start_idx = match.start()
        end_idx = match.end()
        next_section_start = code_pattern.search(md_text[end_idx:])

        section_end = next_section_start.start() + end_idx if next_section_start else len(md_text)
        section = md_text[end_idx:section_end]

        if code_title in summary_dict and code_title in code_keys:
            summary_data = summary_dict[code_title]
            grammar_line = format_summary_block(summary_data, language_counts).split("\n")[1]
            language_line = format_summary_block(summary_data, language_counts).split("\n")[2]

            section = re.sub(
                r"\*\*Grammar patterns:\*\*.*?\n", f"{grammar_line}\n", section
            )
            section = re.sub(
                r"\*\*Language:\*\*.*?\n", f"{language_line}\n", section
            )

        new_lines.append(md_text[last_end:start_idx])
        new_lines.append(md_text[start_idx:end_idx])
        new_lines.append(section)
        last_end = section_end

    new_lines.append(md_text[last_end:])
    return "".join(new_lines)


# === Example Usage ===

digit_df = pd.read_csv("../data/Digit Axial Code Annotations - digit_axial_code_dual_axis.tsv", sep="\t")
conj_df = pd.read_csv("../data/Conjunction Axial Code Annotations - conjunction_axial_codes_final.tsv", sep="\t")
prep_df = pd.read_csv("../data/Preposition Axial Code Annotations - refined_axial_code_labels_updated.tsv", sep="\t")
det_df = pd.read_csv("../data/Determiner Axial Code Anntoations - determiner_axial_code_validation.tsv", sep="\t")

language_counts = compute_language_counts(digit_df, conj_df, prep_df, det_df)

digit_df['code_key'] = digit_df['final_axial_code_role'].str.strip() + " x " + digit_df['final_axial_code_meaning'].str.strip()
digit_summary = summarize_counts_fixed(digit_df, 'code_key')
digit_md = Path("../data/Digit_Selective_Codes_Dual_Axis.md").read_text()
digit_keys = list(digit_summary.keys())
patched_digit_md = patch_markdown(digit_md, digit_summary, digit_keys, language_counts)

conj_summary = summarize_counts_fixed(conj_df, 'final_axial_code')
conj_md = Path("../data/Conjunction_Selective_Code_Summary.md").read_text()
conj_keys = list(conj_summary.keys())
patched_conj_md = patch_markdown(conj_md, conj_summary, conj_keys, language_counts)

prep_summary = summarize_counts_fixed(prep_df, 'final_axial_code')
prep_md = Path("../data/Preposition_Selective_Code_Summary.md").read_text()
prep_keys = list(prep_summary.keys())
patched_prep_md = patch_markdown(prep_md, prep_summary, prep_keys, language_counts)

det_summary = summarize_counts_fixed(det_df, 'final_axial_code')
det_md = Path("../data/Determiner_Selective_Code_Summary.md").read_text()
det_keys = list(det_summary.keys())
patched_det_md = patch_markdown(det_md, det_summary, det_keys, language_counts)

Path("../output/Digit_Selective_Codes_Dual_Axis_UPDATED.md").write_text(patched_digit_md)
Path("../output/Conjunction_Selective_Code_Summary_UPDATED.md").write_text(patched_conj_md)
Path("../output/Preposition_Selective_Code_Summary_UPDATED.md").write_text(patched_prep_md)
Path("../output/Determiner_Selective_Code_Summary_UPDATED.md").write_text(patched_det_md)
