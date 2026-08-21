import os
import sys
import random
import pandas as pd
import numpy as np

# Set fixed random seed for reproducibility
random.seed(42)
np.random.seed(42)

def generate_standard_verification_dataset():
    csv_path = "../Colleges_India.csv"
    if not os.path.exists(csv_path):
        csv_path = "Colleges_India.csv"

    print(f"Reading raw dataset from: {csv_path}")
    df = pd.read_csv(csv_path)

    original_rows = len(df)
    
    # STEP 2: Data Quality Check - Filter invalid/missing essential records
    valid_mask = df['college_name'].notnull() & df['university_name'].notnull() & df['state'].notnull() & df['district'].notnull()
    df_clean = df[valid_mask].copy()
    
    removed_rows = original_rows - len(df_clean)
    remaining_rows = len(df_clean)

    print(f"Data Quality Check Summary:")
    print(f"  Original rows: {original_rows:,}")
    print(f"  Removed rows: {removed_rows:,}")
    print(f"  Remaining valid rows: {remaining_rows:,}")

    # Generate structured claim-evidence verification triples
    records = df_clean.to_dict(orient='records')
    all_states = df_clean['state'].unique().tolist()
    all_districts = df_clean['district'].unique().tolist()
    all_universities = df_clean['university_name'].unique().tolist()
    all_specializations = [s for s in df_clean['specialization'].unique().tolist() if s != 'Not Specified']
    all_managements = [m for m in df_clean['management'].dropna().unique().tolist()]

    processed_data = []
    item_id = 1

    # Take a representative sample of records to build balanced triples
    sampled_records = records[:25000]

    for rec in sampled_records:
        c_name = str(rec['college_name']).strip()
        u_name = str(rec['university_name']).strip()
        state = str(rec['state']).strip()
        district = str(rec['district']).strip()
        c_type = str(rec['college_type']).strip()
        mgmt = str(rec['management']).strip() if pd.notnull(rec['management']) else 'Government'
        spec = str(rec['specialization']).strip() if rec['specialization'] != 'Not Specified' else 'general education'
        address = str(rec['address']).strip() if pd.notnull(rec['address']) else f"{district}, {state}"

        # 1. EVIDENCE CONTEXT
        evidence_text = f"College: {c_name} ({c_type}). University: {u_name} ({rec['university_type']}). Location: {district}, {state} ({rec['location_type']}). Address: {address}. Management: {mgmt}. Specialization: {spec}."

        # 2. SUPPORTS CLAIM (Factually supported by evidence)
        r_type = random.choice(['location', 'affiliation', 'specialization', 'management'])
        if r_type == 'location':
            claim_supports = f"{c_name} is located in {district} district, {state}."
        elif r_type == 'affiliation':
            claim_supports = f"{c_name} is an {c_type} affiliated with {u_name}."
        elif r_type == 'specialization':
            claim_supports = f"{c_name} offers academic specialization in {spec}."
        else:
            claim_supports = f"{c_name} operates under {mgmt} management in {state}."

        processed_data.append({
            "id": f"eb_verif_{item_id}",
            "claim": claim_supports,
            "evidence": evidence_text,
            "label": "SUPPORTS"
        })
        item_id += 1

        # 3. REFUTES CLAIM (Factually contradicts evidence)
        r_ref = random.choice(['wrong_district', 'wrong_state', 'wrong_university', 'wrong_mgmt'])
        if r_ref == 'wrong_district':
            wrong_dist = random.choice([d for d in all_districts if d != district])
            claim_refutes = f"{c_name} is located in {wrong_dist} district, {state}."
        elif r_ref == 'wrong_state':
            wrong_st = random.choice([s for s in all_states if s != state])
            claim_refutes = f"{c_name} is located in {district} district, {wrong_st}."
        elif r_ref == 'wrong_university':
            wrong_u = random.choice([u for u in all_universities if u != u_name])
            claim_refutes = f"{c_name} is directly affiliated with {wrong_u}."
        else:
            wrong_m = random.choice([m for m in all_managements if m != mgmt])
            claim_refutes = f"{c_name} operates under {wrong_m} management."

        processed_data.append({
            "id": f"eb_verif_{item_id}",
            "claim": claim_refutes,
            "evidence": evidence_text,
            "label": "REFUTES"
        })
        item_id += 1

        # 4. NOT_ENOUGH_INFO CLAIM (Asserts unmentioned facts beyond evidence boundary)
        r_nei = random.choice(['tuition', 'founding_year', 'students', 'placement'])
        if r_nei == 'tuition':
            claim_nei = f"{c_name} has an annual tuition fee of Rs. 45,000 for undergraduate courses."
        elif r_nei == 'founding_year':
            claim_nei = f"{c_name} was originally established in 1965 by a royal charter."
        elif r_nei == 'students':
            claim_nei = f"{c_name} has over 3,500 active enrolled students and 150 full-time faculty members."
        else:
            claim_nei = f"{c_name} achieved a 95% campus placement rate in 2023 with top tier tech companies."

        processed_data.append({
            "id": f"eb_verif_{item_id}",
            "claim": claim_nei,
            "evidence": evidence_text,
            "label": "NOT_ENOUGH_INFO"
        })
        item_id += 1

    df_out = pd.DataFrame(processed_data)
    
    # Save to data/processed/verification_dataset.csv
    out_dir_1 = "../data/processed"
    out_dir_2 = "data/processed"
    
    for d in [out_dir_1, out_dir_2]:
        os.makedirs(d, exist_ok=True)
        path = os.path.join(d, "verification_dataset.csv")
        df_out.to_csv(path, index=False)
        print(f"Saved processed dataset to: {os.path.abspath(path)}")

    print(f"\nStandard Verification Dataset Summary:")
    print(f"  Total records: {len(df_out):,}")
    print(f"  Label distribution:")
    print(df_out['label'].value_counts())

if __name__ == "__main__":
    generate_standard_verification_dataset()
