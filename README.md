### Bootstrapping script for Cambridge project

This script performs a bootstrapped Spearman correlation analysis between polygenic risk scores (PRS) and ancestry estimates derived from either [PANE](https://github.com/lm-ut/PANE/tree/main) or Supervised ADMIXTURE. 
It merges PRS, ancestry, and key sample files based on individual IDs, computes the original Spearman correlation along with a 95% bootstrap confidence interval and standard error, and appends the results to a CSV output file (bootstrap_results.csv). 
The script is designed to be run from the command line, specifying input file paths and the comparison type (pane or supervised).


Usage:
python Bootstrapping_man.py --key_samples saample_list --prs_file prs_red_heart_rate.txt --ancestry_file pane_anc0_assignation --comparison_type pane
python Bootstrapping_man.py --key_samples saample_list --prs_file prs_red_heart_rate.txt --ancestry_file superAdmix_anc0_assignation --comparison_type supervised
