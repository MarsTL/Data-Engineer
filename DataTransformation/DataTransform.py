import pandas as pd

# STEP 1: GET THE DATA
df = pd.read_csv("bc_trip259172515_230215.csv")
num_records = len(df)
print(f"\n1. \nNumber of breadcrumb records: {num_records}\n")

# STEP 2: FILTER

print("2. \nUSE DROPPED")
df_full = pd.read_csv("bc_trip259172515_230215.csv")
df_dropped = df_full.drop(columns=["EVENT_NO_STOP", "GPS_SATELLITES", "GPS_HDOP"])

print("Remaining columns after drop():")
print(df_dropped.columns)


# Show a few rows of the filtered DataFrame
print(df_dropped.head())


print("\nUSED USECOLS")
# Use usecols to exclude the unwanted columns during loading
df_filtered = pd.read_csv(
    "bc_trip259172515_230215.csv",
    usecols=lambda col: col not in ["EVENT_NO_STOP", "GPS_SATELLITES", "GPS_HDOP"]
)

print("Remaining columns using usecols:")
print(df_filtered.columns)

print(df_filtered.head())

#STEP 3: DECODE
# OPD_DATE = string 
# ACT_TIME = seconds since midnight
# OPD_DATE -> datetime.date
# ACT_TIME -> timedelta
# OPD_DATE + ACT_TIME = TIMESTAMP column 

print("\n3. \nTIMESTAMP")
df_filtered = pd.read_csv(
    "bc_trip259172515_230215.csv",
    usecols=lambda col: col not in ["EVENT_NO_STOP", "GPS_SATELLITES", "GPS_HDOP"]
)

# OPD_DATE + ACT_TIME = TIMESTAMP column 
df_filtered["TIMESTAMP"] = pd.to_datetime(df_filtered["OPD_DATE"], format="%d%b%Y:%H:%M:%S") + pd.to_timedelta(df_filtered["ACT_TIME"], unit="s")

#print(df_filtered[["OPD_DATE", "ACT_TIME", "TIMESTAMP"]].head())
print(df_filtered.head())

# CONTINUE  
# STEP 3a: Create TIMESTAMP column
print("testttt")
def make_timestamp(row):
    date_str = row["OPD_DATE"].split(":")[0]
    date = pd.to_datetime(date_str, format="%d%b%Y")
    time_offset = pd.to_timedelta(row["ACT_TIME"], unit="s")
    return date + time_offset

df_filtered["TIMESTAMP"] = df_filtered.apply(make_timestamp, axis=1)
df_filtered = df_filtered.drop(columns=["OPD_DATE", "ACT_TIME"])
print("Remaining columns:")
print(df_filtered.columns)
print(df_filtered.head())

#STEP 4: ENHANCE 
# differences calculatiton 
print("\n 4.\n")
df_filtered["dMETERS"] = df_filtered["METERS"].diff()
df_filtered["dTIMESTAMP"] = df_filtered["TIMESTAMP"].diff().dt.total_seconds()

# division by 0 and NaN are avoied 
df_filtered["SPEED"] = df_filtered.apply(
    lambda row: row["dMETERS"] / row["dTIMESTAMP"] if pd.notnull(row["dMETERS"]) and row["dTIMESTAMP"] > 0 else 0,
    axis=1
)
df_filtered = df_filtered.drop(columns=["dMETERS", "dTIMESTAMP"])
print(df_filtered)
print(f"Minimum speed: {df_filtered['SPEED'].min():.2f} m/s")
print(f"Maximum speed: {df_filtered['SPEED'].max():.2f} m/s")
print(f"Average speed: {df_filtered['SPEED'].mean():.2f} m/s")

