# Bootstrapping Script for Cambridge PRS-Ancestry Correlation Analysis

This script performs a bootstrapped Spearman correlation analysis between polygenic risk scores (PRS) and ancestry estimates derived from either [PANE](https://github.com/lm-ut/PANE/tree/main) or Supervised ADMIXTURE. It merges PRS, ancestry, and key sample files based on individual IDs (`IID` column, in all files), computes the original Spearman correlation, and calculates a 95% bootstrap confidence interval and standard error. The results are appended to a CSV output file (`bootstrap_results.csv`).

## Features

- Calculates Spearman correlation between PRS and ancestry estimates
- Performs bootstrapping to compute confidence intervals and standard errors
- Supports input from both PANE and Supervised ADMIXTURE
- Automatically appends results to a cumulative output file

## Requirements

- Input files must contain an `IID` column for individual identification.
- The PRS file must contain a `PRS` column with polygenic risk scores.
- The ancestry file must contain the `NL.AncEMA` column (currently hardcoded).

## Usage

Run from the command line:

```bash
python Bootstrapping_man.py --key_samples sample_list.txt --prs_file prs_red_heart_rate.txt --ancestry_file pane_anc0_assignation.txt --comparison_type pane

python Bootstrapping_man.py --key_samples sample_list.txt --prs_file prs_red_heart_rate.txt --ancestry_file superAdmix_anc0_assignation.txt --comparison_type supervised

