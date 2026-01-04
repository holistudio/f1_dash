import fastf1

fastf1.Cache.enable_cache('../data/cache')

# Load race session
session = fastf1.get_session(year=2019, gp='Hungary', identifier='R')
session.load()

# Access Laps DataFrame
laps = session.laps


# Inspect columns
print(f'Lap Data Columns: {laps.columns}')

# Inspect row count
print(f'Number of rows: {len(laps)}')

# Get list of drivers
drivers = laps['Driver'].unique()
print(f'Drivers: {drivers}\n')

if laps['LapTime'].isna().any():
    n_nat = laps['LapTime'].isna().sum()
    print(f'Number of NaT Lap Times:{n_nat}')
else:
    print('All Lap Times OK')