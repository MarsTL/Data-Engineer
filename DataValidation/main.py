import os
import pandas as pd

# path to employees.csv file
file_path = 'employees.csv'

# file size in bytes
file_size = os.path.getsize(file_path)
print(f"File size: {file_size} bytes")

# load the CSV n count the number of records
df = pd.read_csv(file_path)

# subtract 1 if you only want the number of *data* rows
num_records = len(df)
print(f"Number of records: {num_records}")
