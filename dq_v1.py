import pandas as pd
import plotly.express as px

def check_data_quality(input_excel_file, output_excel_file):
    # Read the Excel file
    xls = pd.read_excel(input_excel_file, sheet_name=None)

    # Prepare a DataFrame to store the issue data
    issue_data = pd.DataFrame(columns=['Sheet', 'Column', 'Issue Type', 'Count'])

    # Loop through each sheet in the Excel file
    for sheet_name, df in xls.items():
        # Check for missing values
        missing_values = df.isnull().sum()
        missing_values = missing_values[missing_values > 0]
        for column, count in missing_values.items():
            issue_data = issue_data.append({'Sheet': sheet_name, 'Column': column, 'Issue Type': 'Missing Values', 'Count': count}, ignore_index=True)

        # Check for duplicates (only counts once per sheet, not per column)
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            issue_data = issue_data.append({'Sheet': sheet_name, 'Column': 'All', 'Issue Type': 'Duplicates', 'Count': duplicates}, ignore_index=True)

        # Check for incorrect types
        for column in df.columns:
            if df[column].dtype == 'object':
                non_numeric = df[column].apply(lambda x: not str(x).isnumeric()).sum()
                if non_numeric > 0:
                    issue_data = issue_data.append({'Sheet': sheet_name, 'Column': column, 'Issue Type': 'Non-numeric in numeric', 'Count': non_numeric}, ignore_index=True)
            else:
                non_numeric = df[column].apply(lambda x: isinstance(x, str)).sum()
                if non_numeric > 0:
                    issue_data = issue_data.append({'Sheet': sheet_name, 'Column': column, 'Issue Type': 'Numeric in non-numeric', 'Count': non_numeric}, ignore_index=True)

    # Generate the Plotly chart
    fig = px.bar(issue_data, x='Sheet', y='Count', color='Issue Type', barmode='group', facet_col='Column', facet_col_wrap=2, height=600, title='Data Quality Issues')
    fig.show()

    # Generate the text summary
    summary = issue_data.groupby(['Sheet', 'Column', 'Issue Type'])['Count'].sum().to_string()
    print(summary)

    # Write the issue data to the Excel file
    issue_data.to_excel(output_excel_file, index=False)

# Usage
check_data_quality('input_file.xlsx', 'output_file.xlsx')
