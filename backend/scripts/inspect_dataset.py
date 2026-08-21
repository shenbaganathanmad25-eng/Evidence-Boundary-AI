import os
import sys
import pandas as pd
import numpy as np

def inspect_dataset():
    csv_path = "../Colleges_India.csv"
    if not os.path.exists(csv_path):
        csv_path = "Colleges_India.csv"

    print(f"Loading dataset from: {csv_path}")
    df = pd.read_csv(csv_path)

    report_lines = []
    report_lines.append("# DATASET INSPECTION REPORT")
    report_lines.append("## Evidence Boundary AI — Verification Dataset\n")

    report_lines.append("### 1. File Metadata")
    report_lines.append(f"- **Filename**: `{os.path.basename(csv_path)}`")
    report_lines.append(f"- **File Format**: CSV (Comma Separated Values)")
    report_lines.append(f"- **Number of Rows**: `{len(df):,}`")
    report_lines.append(f"- **Number of Columns**: `{len(df.columns)}`")

    report_lines.append("\n### 2. Schema & Data Types")
    report_lines.append("| Column Index | Column Name | Data Type | Non-Null Count | Missing Count | % Missing |")
    report_lines.append("|---|---|---|---|---|---|")
    
    for idx, col in enumerate(df.columns):
        non_null = df[col].notnull().sum()
        missing = df[col].isnull().sum()
        pct_missing = (missing / len(df)) * 100
        dtype = str(df[col].dtype)
        report_lines.append(f"| {idx+1} | `{col}` | {dtype} | {non_null:,} | {missing:,} | {pct_missing:.2f}% |")

    # Duplicate check
    duplicate_rows = df.duplicated().sum()
    report_lines.append(f"\n### 3. Duplicate Rows Check")
    report_lines.append(f"- **Total Exact Duplicate Rows**: `{duplicate_rows:,}`")

    # Unique values
    report_lines.append("\n### 4. Cardinality & Unique Values per Column")
    report_lines.append("| Column Name | Unique Values Count | Top Value Example |")
    report_lines.append("|---|---|---|")
    for col in df.columns:
        n_unique = df[col].nunique(dropna=False)
        top_val = str(df[col].mode()[0]) if not df[col].empty else "N/A"
        report_lines.append(f"| `{col}` | {n_unique:,} | `{top_val[:40]}` |")

    # Display 10 sample records
    report_lines.append("\n### 5. Sample Records (First 10 Rows)")
    report_lines.append("| College Name | University Name | State | District | College Type | Management | Specialization |")
    report_lines.append("|---|---|---|---|---|---|---|")
    
    for idx, row in df.head(10).iterrows():
        c_name = str(row['college_name']).replace('|', '/')
        u_name = str(row['university_name']).replace('|', '/')
        state = str(row['state'])
        district = str(row['district'])
        ctype = str(row['college_type'])
        mgmt = str(row['management'])
        spec = str(row['specialization'])
        report_lines.append(f"| `{c_name[:30]}` | `{u_name[:30]}` | {state} | {district} | {ctype} | {mgmt} | {spec} |")

    # Candidate column mapping explanation
    report_lines.append("\n### 6. Evidence Verification Column Mapping Strategy")
    report_lines.append("The raw `Colleges_India.csv` dataset contains tabular metadata on Indian higher education institutions.")
    report_lines.append("To train the **Evidence Boundary AI Verification Model**, structured claim-evidence verification pairs are constructed:")
    report_lines.append("- **Evidence Context**: Synthesized from factual record fields (`college_name`, `university_name`, `state`, `district`, `college_type`, `management`, `specialization`, `address`).")
    report_lines.append("- **Claim**: Structured assertion regarding college location, affiliation, type, specialization, or unverified external facts.")
    report_lines.append("- **Target Label**: Classified into 3 standard verification classes:")
    report_lines.append("  1. `SUPPORTS`: Claim directly matches factual record.")
    report_lines.append("  2. `REFUTES`: Claim contradicts factual record (e.g. wrong district, wrong state, wrong university affiliation).")
    report_lines.append("  3. `NOT_ENOUGH_INFO`: Claim makes assertions outside available evidence boundary (e.g., student capacity, tuition fees, founding date).")

    report_content = "\n".join(report_lines)

    # Save to dataset_report.md
    out_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(out_dir)
    report_path = os.path.join(project_root, "dataset_report.md")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)

    print(f"Dataset inspection complete. Written report to: {report_path}")

if __name__ == "__main__":
    inspect_dataset()
