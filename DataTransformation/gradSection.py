import pandas as pd

'''
dMETERS[row 1] = METERS[1] - METERS[0] = 40 - 4223 = -4183

dTIMESTAMP = TIMESTAMP[1] - TIMESTAMP[0]
           = 2023-02-15 05:41:09 - 2023-02-15 07:07:21
           = -1 hour, -26 minutes, -12 seconds
           = -5172 seconds
dSECONDS[row 1] = -5172

SPEED = dMETERS / dSECONDS
      = -4183 / -5172
      = 0.81 m/s
      = 0
      
'''
df = pd.read_csv("bc_veh4223_230215.csv")
num_records = len(df)
print(f"\nNumber of breadcrumb records: {num_records}\n")


#  OPD_DATE + ACT_TIME -> TIMESTAMP
df["OPD_DATE"] = pd.to_datetime(df["OPD_DATE"].str[:9], format="%d%b%Y")
df["TIMESTAMP"] = df["OPD_DATE"] + pd.to_timedelta(df["ACT_TIME"], unit="s")

# Sort by VEHICLE_ID and TIMESTAMP
df.sort_values(by=["VEHICLE_ID", "TIMESTAMP"], inplace=True)

# Calculate dMETERS and dSECONDS
df["dMETERS"] = df["METERS"].diff()
df["dSECONDS"] = df["TIMESTAMP"].diff().dt.total_seconds()

# Calculate SPEED in m/s
df["SPEED"] = df.apply(lambda row: row["dMETERS"] / row["dSECONDS"] if pd.notnull(row["dMETERS"]) and row["dSECONDS"] > 0 else 0, axis=1)

# Drop columns
df.drop(columns=["dMETERS", "dSECONDS", "OPD_DATE", "ACT_TIME"], inplace=True)

#After sorting the rows by timestamp and calculating new columns, 
# the original index no longer maked sense. So,reseting it to start from 0 again,
# discarding the old one.
df.reset_index(drop=True, inplace=True)

pd.set_option("display.max_columns", None)
# Print a preview with SPEED
print(df[[ "EVENT_NO_TRIP", "VEHICLE_ID", "TIMESTAMP", "METERS", "SPEED", "GPS_LATITUDE", "GPS_LONGITUDE" ]].head())
print("tttttt")
print(df.columns)

#vehicle 4223 on Feb 15, 2023
df_4223 = df[df["VEHICLE_ID"] == 4223]
max_speed_row = df_4223.loc[df_4223["SPEED"].idxmax()]

max_speed = max_speed_row["SPEED"]
max_time = max_speed_row["TIMESTAMP"]
max_location = (max_speed_row["GPS_LATITUDE"], max_speed_row["GPS_LONGITUDE"])
median_speed = df_4223["SPEED"].median()

print(f"\nMaximum speed: {max_speed:.2f} m/s")
print(f"Occurred at: {max_time}")
print(f"Location: Latitude {max_location[0]}, Longitude {max_location[1]}")
print(f"Median speed: {median_speed:.2f} m/s")
