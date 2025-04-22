import pandas as pd 
import matplotlib.pyplot as plt

# path to employees.csv file
file_path = 'employees.csv'

# load the CSV with dataframe 
df = pd.read_csv(file_path)

# checks if any records have a missing (null or empty) name field
# 1st arg checks if the name value is NaN (missing/null) in each row
# converts each value in the name column to a string -> .strip removes whitespaces -> 
# checks of string is emty 
invalid_name = df['name'].isnull() | (df['name'].astype(str).str.strip() == '')
# counts how many true (invalidated name) value there are 
num_invalid_names = invalid_name.sum()
print(f"Records with missing or blank 'name': {num_invalid_names}")

# existence assertion: salary must not be null 
# non-null -> isnull
# non-blank -> convert to string -> .str.strip() removes whitespace -> compare blank
invalid_salary = df['salary'].isnull() | (df['salary'].astype(str).str.strip() == '')
num_invalid_salaries = invalid_salary.sum()
print(f"Records with missing or blank 'salary': {num_invalid_salaries}")


# limit assertion: every employee was hired no earlier than 2015 
# convert hire_date to datetime object 
# if value can't be converted to a date replaced with NaT (not a time)
df['hire_date'] = pd.to_datetime(df['hire_date'], errors='coerce')
#print(df['hire_date'])

# hire_date must be >= 2015-01-01
invalid_hire_dates = df['hire_date'] < pd.to_datetime('2015-01-01')
num_invalid_hires = invalid_hire_dates.sum()
print(f"Records with hire_date before 2015: {num_invalid_hires}")

# salary must be between $50,000 - $150,000
# make sure salary are numbers 
df['salary'] = pd.to_numeric(df['salary'], errors='coerce')
invalid_salary_limit = (df['salary'] < 50000) | (df['salary'] > 150000)
num_invalid_salary_limit = invalid_salary_limit.sum()
print(f"Records with salary outside $50,000–$150,000 range: {num_invalid_salary_limit}")

# intra-record Assertion ->  consistency in the record  
# each employee was born before they were hired 
# Convert birth_date to datetime (if not already done)
df['birth_date'] = pd.to_datetime(df['birth_date'], errors='coerce')
invalid_birth = df['birth_date'] >= df['hire_date']
num_invalid_birth = invalid_birth.sum()
print(f"Records where birth date is not before hire date: {num_invalid_birth}")

# phone number with at least 10 digits
df['digits_in_phone'] = df['phone'].astype(str).str.replace(r'\D', '', regex=True) 
invalid_phone_num = df['digits_in_phone'].str.len() < 10
num_invalid_phone_num = invalid_phone_num.sum()

print(f"Records with phone numbers containing at least than 10 digits: {num_invalid_phone_num}")

# Inter-record Assertion
# each employee has a manager who is a known employee
# If reports_to is filled out, it must match an existing eid in the dataset.
# Exclude rows where reports_to is blank or null
reports_to_null = df['reports_to'].notnull() & (df['reports_to'] != '')
# set of valid EIDs
eids = set(df['eid'].astype(str))
# ~ flips the result, so True where the reports_to value does not match any known eid.
managers = ~df.loc[reports_to_null, 'reports_to'].isin(eids)
num_invalid_managers = managers.sum()
print(f"Records with unknown managers: {num_invalid_managers}")


# all employees should have their own unique ID
# .duplicated() checks for repeated values in the eid column.
# keep=False Marks all duplicates as True
duplicate = df['eid'].duplicated(keep=False)
num_duplicate = duplicate.sum()
#print(df.loc[duplicate_eids, 'eid'].value_counts())
print(f"Records with duplicate employee IDs: {num_duplicate}")

# Summary Assertion
# each city has more than one employee
# group the same ciy and count them 
city = df['city'].value_counts()
#filter to cities with only one employee.
cities_one_employee = city[city == 1]
print(f"Records with cities with only one employee: {len(cities_one_employee)}")

# a job title needs at least 2 employees
title_num = df['title'].value_counts()
titles_one_employee = title_num[title_num == 1]
print(f"Record with titles held by only one employee: {len(titles_one_employee)}")

#Statistical Assertion
#the salaries are normally distributed

# Clean and convert the salary column
salaries = df['salary'].dropna()
salaries = salaries[salaries.astype(str).str.strip() != ''].astype(float)

# Find min and max salary
min_salary = salaries.min()
max_salary = salaries.max()

print(f"Lowest salary: ${min_salary:,.2f}")
print(f"Highest salary: ${max_salary:,.2f}")

plt.figure(figsize=(10, 6))
plt.hist(salaries, bins=20, range=(min_salary, max_salary), color='black', edgecolor='black')

plt.title('Salary Distribution')
plt.xlabel('Salary')
plt.ylabel('Number of Employees')
plt.grid(True)
plt.tight_layout()

plt.show()


#median salary should be between $50,000-$150,000
median_salary = salaries.median()
min_expected = 50000
max_expected = 150000
valid_median = min_expected <= median_salary <= max_expected

# Output result
print(f"Median salary: ${median_salary:,.2f}")
if valid_median:
    print("Median salary is within the expected range.")
else:
    print("Median salary is outside the expected range.")
