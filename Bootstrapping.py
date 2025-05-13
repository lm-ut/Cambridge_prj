#!/usr/bin/env python
# coding: utf-8

# USAGE 

#python bootstrapping.py key_samples.txt prs_file.txt ancestry_file.txt pane
#python bootstrapping.py key_samples.txt prs_file.txt ancestry_file.txt supervised


import argparse
import numpy as np
import os 
import pandas as pd
from scipy.stats import spearmanr
from tqdm import tqdm

# Function to check if a required column exists in a DataFrame
def check_column_exists(df, column_name):
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' does not exist in the provided file.")
    else:
        print(f"Column '{column_name}' found in the data.")

# Function to perform bootstrapping and calculate correlation
def bootstrap_correlation(anc_values, prs_values, n_boot=10000):
    n = len(anc_values)
    boot_rhos = []

    # Perform bootstrapping
    for _ in tqdm(range(n_boot), desc="Bootstrapping"):
        idx = np.random.choice(n, n, replace=True)
        rho, _ = spearmanr(anc_values[idx], prs_values[idx])
        boot_rhos.append(rho)

    boot_rhos = np.array(boot_rhos)

    # Original Spearman correlation
    orig_rho, orig_p = spearmanr(anc_values, prs_values)

    # Bootstrap CI and SE
    ci_lower = np.percentile(boot_rhos, 2.5)
    ci_upper = np.percentile(boot_rhos, 97.5)
    se = np.std(boot_rhos)

    return orig_rho, orig_p, ci_lower, ci_upper, se, boot_rhos


# Function to process a PRS file and its correlation with a specific trait
def process_prs_file(prs_file_path, anc_column_name, key_file, ancestry_file, comparison_type):
    prs_file = pd.read_csv(prs_file_path, delimiter='\t')

	
    # Merge with the key and trait files
    Key = pd.merge(key_file, ancestry_file, on='IID', how='inner')
    Key_PRS = pd.merge(Key, prs_file, on='IID', how='inner')

    # Check if necessary columns exist
    check_column_exists(Key_PRS, 'PRS')
    check_column_exists(Key_PRS, anc_column_name)  # Trait column (PANE/Supervised)

    # Extract values for correlation
    anc_values = Key_PRS[anc_column_name].values
    prs_values = Key_PRS['PRS'].values

    # Perform bootstrapping and correlation
    orig_rho, orig_p, ci_lower, ci_upper, se, boot_rhos = bootstrap_correlation(anc_values, prs_values)

    # Store the results in a dictionary (for later saving)
    results = {
        'PRS_File': prs_file_path,
        'Ancestry': anc_column_name,
        'Comparison_Type': comparison_type,
        'Spearman_ρ': round(orig_rho, 4),
        'p-value': orig_p,
        'Bootstrap_95%_CI': f"({ci_lower:.4f}, {ci_upper:.4f})",
        'Bootstrap_SE': round(se, 4)
    }

    return results


def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description="Run bootstrapping analysis for PRS and trait correlation.")
    parser.add_argument("--key_samples", help="Path to the KEY_Samples file")
    parser.add_argument("--prs_file", help="Path to the PRS file")
    parser.add_argument("--ancestry_file", help="Path to the ancestry file (PANE or Supervised Admixture)")
    parser.add_argument("--comparison_type", choices=["pane", "supervised"], help="Type of comparison to run: 'pane' or 'supervised'")
    
    args = parser.parse_args()

    # Load key and trait files
    key_samples = pd.read_csv(args.key_samples, delimiter='\t')
    prs_file = pd.read_csv(args.prs_file, delimiter='\t')
    ancestry_file = pd.read_csv(args.ancestry_file, delimiter='\t')
    
    #print(key_samples.head(10))
    #print(prs_file.head(10))
    #print(ancestry_file.head(10))
    
    
    # Initialize a list to store all results
    all_results = []

    # Determine which comparison to run based on the argument
    if args.comparison_type == "pane":
        print("Running analysis for PANE vs PRS comparisons.")
        anc_column_name = 'NL.AncEMA'  # PANE column name
    else:  # supervised
        print("Running analysis for Supervised Admixture vs PRS comparisons.")
        anc_column_name = 'NL.AncEMA'  # Supervised admixture column name

    # Run the script for the PRS file and the chosen trait column
    print(f"Processing {args.prs_file} with {anc_column_name}...")
    result = process_prs_file(args.prs_file, anc_column_name, key_samples, ancestry_file, args.comparison_type)
    all_results.append(result)

    # Convert the results to a DataFrame for easy viewing or saving
    results_df = pd.DataFrame(all_results)

    # Appending results to the output file
    output_file = 'bootstrap_results.csv'
    if os.path.exists(output_file):
        results_df.to_csv(output_file, mode='a', index=False, header=False)
    else:
        results_df.to_csv(output_file, index=False)

    print("Processing complete. Results saved to 'bootstrap_results.csv'.")


if __name__ == "__main__":
    main()

