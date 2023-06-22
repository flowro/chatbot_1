import pandas as pd

def check_data_quality(excel_file):
    # Read the Excel file
    xls = pd.read_excel(excel_file, sheet_name=None)

    # Create a dictionary to store all the issues
    all_issues = {}

    # Loop through each sheet in the Excel file
    for sheet_name, df in xls.items():
        # Create a dictionary to store issues for this sheet
        issues = {}

        # Check for missing values
        missing_values = df.isnull().sum()
        issues['Missing values'] = missing_values[missing_values > 0]

        # Check for duplicates
        duplicates = df.duplicated().sum()
        issues['Duplicates'] = f'Total duplicate rows: {duplicates}'

        # Check for incorrect types
        incorrect_types = {}
        for column in df.columns:
            if df[column].dtype == 'object':
                non_numeric = df[column].str.isnumeric().sum()
                if non_numeric > 0:
                    incorrect_types[column] = f'Non-numeric entries: {non_numeric}'
            else:
                non_numeric = df[column].apply(lambda x: isinstance(x, str)).sum()
                if non_numeric > 0:
                    incorrect_types[column] = f'Non-numeric entries: {non_numeric}'
        issues['Incorrect types'] = incorrect_types

        # Store the issues for this sheet
        all_issues[sheet_name] = issues

    # Return the issues
    return all_issues

# Usage
issues = check_data_quality('your_file.xlsx')

# Print issues
for category, issue in issues.items():
    print(category)
    if isinstance(issue, pd.Series):
        print(issue.to_string())
    else:
        print(issue)
#This is a very basic data quality check. For more complex checks, you might want to check out libraries like pandas-profiling or great_expectations.
