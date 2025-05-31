import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import io
from scipy.stats import binomtest
from scipy.stats import ttest_ind
from scipy.stats import chi2_contingency

# Load HTML content
with open("trimet_stopevents_2022-12-07.html", "r") as f:
    html_content = f.read()

# Read all tables with pandas
tables = pd.read_html(io.StringIO(html_content))

# DataFrame
combined_df = pd.concat(tables, ignore_index=True)
service_date = datetime.strptime("2022-12-07", "%Y-%m-%d")

# get required columns 
stops_df = pd.DataFrame()
stops_df["trip_id"] = combined_df["trip_number"]
stops_df["vehicle_number"] = combined_df["vehicle_number"]
stops_df["location_id"] = combined_df["location_id"]
stops_df["ons"] = combined_df["ons"]
stops_df["offs"] = combined_df["offs"]

# arrive_time to datetime
stops_df["tstamp"] = combined_df["arrive_time"].apply(
    lambda sec: service_date + timedelta(seconds=int(sec))
)
stops_df = stops_df[["trip_id", "vehicle_number", "tstamp", "location_id", "ons", "offs"]]
print("rowscolumns:", stops_df.shape)
print(stops_df.head())

#a
num_vehicles = stops_df["vehicle_number"].nunique()
print("A. Number of unique vehicles:", num_vehicles)

#b
locations = stops_df["location_id"].nunique()
print("B. Number of unique stop locations:", locations)

#c
min = stops_df["tstamp"].min()
max = stops_df["tstamp"].max()
print("C. min:", min, "max", max)

#d
num_ons = stops_df[stops_df["ons"] >= 1].shape[0]
print("D. Stop events with at least one boarding:", num_ons)

#e
total = stops_df.shape[0]
percent = (num_ons / total) * 100
print(f"E. Percentage of stop events with boardings: {percent:.2f}%")

#3validate for 6913 location 
locate_6913= stops_df[stops_df["location_id"] == 6913]
num_stops = locate_6913.shape[0]
unique_vehicles_6913 = locate_6913["vehicle_number"].nunique()
boarding_6913 = locate_6913[locate_6913["ons"] >= 1].shape[0]
percent_6913 = (boarding_6913 / num_stops) * 100 if num_stops else 0

print("\nLocation 6913:")
print(f"Stops made: {num_stops}")
print(f"Buses: {unique_vehicles_6913}")
print(f"% with boardings: {percent_6913:.2f}%")


# 3validate for 4062
car_4062 = stops_df[stops_df["vehicle_number"] == 4062]
stops_4062 = car_4062.shape[0]
board_4062 = car_4062["ons"].sum()
deboard_4062 = car_4062["offs"].sum()
stops_ons_4062 = car_4062[car_4062["ons"] >= 1].shape[0]
percent_4062 = (stops_ons_4062 / stops_4062) * 100 if stops_4062 else 0

print("\nVehicle 4062:")
print(f"Stops made: {stops_4062}")
print(f"Passengers boarded: {board_4062}")
print(f"Passengers deboard: {deboard_4062}")
print(f"% of stops with boardings: {percent_4062:.2f}% \n")

# Bias 
p_system = num_ons / total 
grouped = stops_df.groupby("vehicle_number")
biased_car = []
for vehicle_id, group in grouped:
    n = group.shape[0]                            
    g = group[group["ons"] >= 1].shape[0]        

    # Binomial with p_system
    result = binomtest(g, n, p=p_system, alternative="two-sided")
    if result.pvalue < 0.05:
        biased_car.append({
            "vehicle_number": vehicle_id,
            "stops": n,
            "stops_with_boarding": g,
            "boarding_rate": round(g / n, 3),
            "p_value": round(result.pvalue, 5)
        })
# DF
biased_df = pd.DataFrame(biased_car)
biased_df = biased_df.sort_values(by="p_value")
print(biased_df.head(20))

# Group RELPOS values by vehicle_id
relpos= pd.read_csv("trimet_relpos_2022-12-07.csv")
all_relpos = relpos["RELPOS"].dropna().values
print(f"\n5A. Loaded RELPOS values for {len(all_relpos)} records.")

vehicle_relpos_groups = relpos.groupby("VEHICLE_NUMBER")["RELPOS"]
biased_gps = []
for vehicle_number, vehicle_relpos in vehicle_relpos_groups:
    vehicle_relpos = vehicle_relpos.dropna().values
    t_stat, p_value = ttest_ind(vehicle_relpos, all_relpos, equal_var=False)

    if p_value < 0.005:
        biased_gps.append({
            "vehicle_number": vehicle_number,
            "num_points": len(vehicle_relpos),
            "mean_relpos": round(np.mean(vehicle_relpos), 5),
            "p_value": round(p_value, 6)
        })

biased_gps_df = pd.DataFrame(biased_gps).sort_values(by="p_value")
print("\n5B. Vehicles with biased GPS RELPOS:")
print(biased_gps_df.head(20))


#graduaate 
total_ons = stops_df["ons"].sum()
total_offs = stops_df["offs"].sum()
print("\n6B. System-wide totals:")
print(f"Total ons (board): {total_ons}")
print(f"Total offs (deboard): {total_offs}")


biased_offs = []
grouped = stops_df.groupby("vehicle_number")

for vehicle_id, group in grouped:
    ons = group["ons"].sum()
    offs = group["offs"].sum()
    rest_offs = total_offs - offs
    rest_ons = total_ons - ons
    contingency_table = [[offs, ons],
                         [rest_offs, rest_ons]]

    chi2, p, _, _ = chi2_contingency(contingency_table)
    if p < 0.05:
        biased_offs.append({
            "vehicle_number": vehicle_id,
            "vehicle_ons": ons,
            "vehicle_offs": offs,
            "p_value": round(p, 6)
        })

biased_offs_df = pd.DataFrame(biased_offs).sort_values(by="p_value")
print("\n6c. Chi, ratio p < 0.05")
print(biased_offs_df.head(20))

