import pandas as pd

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
#print("Statewide Unallocated in Cases DataFrame:\n", cases_df[cases_df['County Name'] == "Statewide Unallocated"])
#print("Statewide Unallocated in Deaths DataFrame:\n", deaths_df[deaths_df['County Name'] == "Statewide Unallocated"])
cases_df = cases_df[cases_df['County Name'] != "Statewide Unallocated"]
deaths_df = deaths_df[deaths_df['County Name'] != "Statewide Unallocated"]
print(f"\nRemaining rows in Cases DataFrame: {cases_df.shape[0]}")
print(f"Remaining rows in Deaths DataFrame: {deaths_df.shape[0]}")

# 5. challenge 3

