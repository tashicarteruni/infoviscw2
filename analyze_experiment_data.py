import pandas as pd
from scipy.stats import ttest_ind, chi2_contingency
import os

def get_next_filename(base_filepath, num_files):
    for i in range(1, num_files + 1):
        filepath = f'{base_filepath}_{i}.csv'
        if os.path.exists(filepath):
            yield filepath

def analyze_data(base_filepath, num_files):
    response_time_ttests = []
    error_ratios = []
    chi2_tests = []

    for filepath in get_next_filename(base_filepath, num_files):
        data = pd.read_csv(filepath)

        # Response Time Analysis
        line_times = data[data['Chart Type'] == 'line']['Time Taken (seconds)']
        area_times = data[data['Chart Type'] == 'area']['Time Taken (seconds)']
        ttest_result = ttest_ind(line_times, area_times, nan_policy='omit')
        response_time_ttests.append(ttest_result)

        # Error Ratio Analysis
        data['Error'] = (data['User Answer'] != data['Question Answered Correctly']).astype(int)
        error_summary = data.groupby('Chart Type')['Error'].agg(['sum', 'count'])
        error_summary['Error Ratio'] = error_summary['sum'] / error_summary['count']
        error_ratios.append(error_summary)

        # Chi-squared Test
        chi2, p, _, _ = chi2_contingency(error_summary[['sum', 'count']])
        chi2_tests.append((chi2, p))

    return response_time_ttests, error_ratios, chi2_tests

def main():
    base_filepath = 'experiment_data' # Replace with your file path
    num_files = 2

    ttests, error_ratios, chi2_tests = analyze_data(base_filepath, num_files)

    print("T-Test Results for Response Times:")
    for i, ttest in enumerate(ttests, 1):
        print(f"File {i}: t-statistic = {ttest.statistic}, p-value = {ttest.pvalue}")

    print("\nError Ratios:")
    for i, error_ratio in enumerate(error_ratios, 1):
        print(f"File {i}:\n{error_ratio}\n")

    print("Chi-Squared Test Results:")
    for i, (chi2, p) in enumerate(chi2_tests, 1):
        print(f"File {i}: Chi-square = {chi2}, p-value = {p}")

if __name__ == "__main__":
    main()
