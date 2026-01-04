import fastf1

fastf1.Cache.enable_cache('../data/cache')

# Load race session
session = fastf1.get_session(year=2019, gp='Hungary', identifier='R')
session.load()

# Access Laps DataFrame
laps = session.laps


# Inspect columns
print(f'\nLap Data Columns: {laps.columns}')

# Inspect row count
print(f'Number of rows: {len(laps)}')

# Get list of drivers
drivers = laps['Driver'].unique()
print(f'Drivers: {drivers}\n')

# Convert `LapTime` from Timedelta to float seconds
laps['LapTime'] = laps['LapTime'].dt.total_seconds()

# Check for NaT values in LapTime
if laps['LapTime'].isna().any():
    n_nat = laps['LapTime'].isna().sum()
    print(f'Number of NaT Lap Times:{n_nat}')
else:
    print('All Lap Times non-NaT')
    column_dtypes = laps['LapTime'].dtypes
    print(f'dtypes: {column_dtypes}\n')

# Drop rows with NaT LapTimes
valid_laps = laps[laps['LapTime'].notna()]

# Group by `Driver` and compute cumulative sum of lap time seconds
valid_laps['CumulativeLapTime'] = valid_laps.groupby('Driver')['LapTime'].cumsum()

# Check cumulative time should increase monotonically per driver
is_monotonic_inc = valid_laps.groupby('Driver')['CumulativeLapTime'].diff().dropna().ge(0).all()

if is_monotonic_inc:
    print('All Driver Cumulative Lap Times Monotonically Increasing')
else:
    print('Non-increasing Cumulative Lap Times')
    filter = valid_laps.groupby('Driver')['CumulativeLapTime'].diff().dropna().ge(0) != True
    print(valid_laps[filter][['Driver','LapNumber','LapTime','CumulativeLapTime']])