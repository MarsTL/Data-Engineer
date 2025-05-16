import pandas as pd
from us_state_abbrev import abbrev_to_us_state
import seaborn as sns
import matplotlib.pyplot as plt

#pip3 install seaborn


# Read the datasets
cases_df = pd.read_csv("covid_confirmed_usafacts.csv")
deaths_df = pd.read_csv("covid_deaths_usafacts.csv")
census_df = pd.read_csv("acs2017_county_data.csv")

# show the first few rows to confirm the data was read correctly
# print(cases_df.head())
# print(deaths_df.head())
# print(census_df.head())
print(f"Cases DataFrame: {cases_df.shape[0]}")
print(f"Deaths DataFrame: {deaths_df.shape[0]}")
print(f"Census DataFrame: {census_df.shape[0]}")

# 2b. trim cases_df, death_df for county name, state, 2023-07-23
cases_df = cases_df[['County Name', 'State', '2023-07-23']]
deaths_df = deaths_df[['County Name', 'State', '2023-07-23']]
census_df = census_df[['County', 'State', 'TotalPop', 'IncomePerCap', 'Poverty', 'Unemployment']]
#print(f"Covid Confirmed Usafacts\n {cases_df.head()}")
#print(f"Covid Deaths Usafacts\n {cases_df.head()}")
#print(census_df.head())
 
# Display the column headers for each DataFrame
print("Cases DataFrame Columns:", cases_df.columns.tolist())
print("Deaths DataFrame Columns:", deaths_df.columns.tolist())
print("Census DataFrame Columns:", census_df.columns.tolist())

# 3 challange 1, extra space remove fro cases_df and deaths_df
cases_df['County Name'] = cases_df['County Name'].str.strip()
deaths_df['County Name'] = deaths_df['County Name'].str.strip()

# look for "Washington County" in both DataFrames
washington_cases = cases_df[cases_df['County Name'] == "Washington County"]
washington_deaths = deaths_df[deaths_df['County Name'] == "Washington County"]
print("\nWashington County in Cases DataFrame:\n", washington_cases)
print("\nWashington County in Deaths DataFrame:\n", washington_deaths)

# #of country named washington county 
num_washington_cases = washington_cases.shape[0]
num_washington_deaths = washington_deaths.shape[0]
print(f"\nNumber of 'Washington County' entries in Cases DataFrame: {num_washington_cases}")
print(f"Number of 'Washington County' entries in Deaths DataFrame: {num_washington_deaths}")

# 4. challenge 2, remove "Statewide Unallocated" Records
cases_df = cases_df[cases_df['County Name'] != "Statewide Unallocated"]
deaths_df = deaths_df[deaths_df['County Name'] != "Statewide Unallocated"]
print(f"\nRemaining rows in Cases DataFrame: {cases_df.shape[0]}")
print(f"Remaining rows in Deaths DataFrame: {deaths_df.shape[0]}")

# 5. challenge 3
cases_df['State'] = cases_df['State'].map(abbrev_to_us_state)
deaths_df['State'] = deaths_df['State'].map(abbrev_to_us_state)
print("\nFirst few rows of Cases DataFrame after state name alignment:\n", cases_df.head())#works
print("\nFirst few rows of Deaths DataFrame after state name alignment:\n", deaths_df.head())#works 

# 6. challenge 4
# create key column with string concatenation of county aand state 
cases_df['key'] = cases_df['County Name'] + ", " + cases_df['State']
deaths_df['key'] = deaths_df['County Name'] + ", " + deaths_df['State']
census_df['key'] = census_df['County'] + ", " + census_df['State']

cases_df = cases_df.set_index('key')
deaths_df = deaths_df.set_index('key')
census_df = census_df.set_index('key')
#print("\nIndex of Cases DataFrame:\n", cases_df.index)
#print("\nIndex of Deaths DataFrame:\n", deaths_df.index)
#print("\nIndex of Census DataFrame:\n", census_df.index)
print("\nFirst few rows of Census DataFrame with 'key' as index:\n", census_df.head())

# 7. challenge 5 rename 2023-07-23 column to cases and deaths 
# '2023-07-23' to Cases in cases_df
# '2023-07-23' to Death in deaths_df
cases_df = cases_df.rename(columns={'2023-07-23': 'Cases'})
deaths_df = deaths_df.rename(columns={'2023-07-23': 'Deaths'})
print("\nCases DataFrame Columns:", cases_df.columns.values.tolist())
print("\nDeaths DataFrame Columns:", deaths_df.columns.values.tolist())

#8 join 
join_df = census_df.join(cases_df[['Cases']], how='inner')
join_df = join_df.join(deaths_df[['Deaths']], how='inner')
print("\nFirst few rows of join_df after integration:\n", join_df.head())
join_df['CasesPerCap'] = join_df['Cases'] / join_df['TotalPop']
join_df['DeathsPerCap'] = join_df['Deaths'] / join_df['TotalPop']
print("\nFirst few rows of join_df with CasesPerCap and DeathsPerCap:\n", join_df.head())
print("\nNumber of rows in join_df:", join_df.shape[0])

# 9 correlation matrix 
correlation_matrix = join_df.corr(numeric_only=True)
print("\nCorrelation Matrix:\n", correlation_matrix)

# 10 visualiza 
# Create the heatmap
#plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)

# Title and display the heatmap
plt.title('Correlation Matrix Heatmap')
plt.show()
