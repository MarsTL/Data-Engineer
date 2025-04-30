import pandas as pd

# STEP 1: GET THE DATA
df = pd.read_csv("bc_trip259172515_230215.csv")
num_records = len(df)
print(f"\nNumber of breadcrumb records: {num_records}\n")

# STEP 2: FILTER
print("USE DROPPED")
df_full = pd.read_csv("bc_trip259172515_230215.csv")
df_dropped = df_full.drop(columns=["EVENT_NO_STOP", "GPS_SATELLITES", "GPS_HDOP"])

print("Remaining columns after drop():")
print(df_dropped.columns)


# Show a few rows of the filtered DataFrame
print(df_dropped.head())


print("\nUSED USECOL")
# Use usecols to exclude unwanted columns during loading
df_filtered = pd.read_csv(
    "bc_trip259172515_230215.csv",
    usecols=lambda col: col not in ["EVENT_NO_STOP", "GPS_SATELLITES", "GPS_HDOP"]
)

print("Remaining columns using usecols:")
print(df_filtered.columns)

print(df_filtered.head())