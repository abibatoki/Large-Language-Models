import pandas as pd

# Specify the path to your CSV file
csv_file_path = r'C:\Users\user\Downloads\stories.csv'  # Update with the actual path to your CSV file

# Read the CSV file into a DataFrame using the header row as column names
df = pd.read_csv(csv_file_path, header=None)

# Display the DataFrame
print(df)
