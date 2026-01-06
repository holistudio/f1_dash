import os
import fastf1

# Configure cache relative to this script to ensure it works from any CWD
script_dir = os.path.dirname(os.path.abspath(__file__))
cache_path = os.path.join(script_dir, '../data/cache')
fastf1.Cache.enable_cache(cache_path)

def main():
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
        print(f'Number of NaT Lap Times: {n_nat}')
    else:
        print('All Lap Times non-NaT')
        column_dtype = laps['LapTime'].dtype
        print(f'dtype: {column_dtype}\n')

    # Drop rows with NaT LapTimes
    # Use .copy() to avoid SettingWithCopyWarning
    valid_laps = laps[laps['LapTime'].notna()].copy()

    # Group by `Driver` and compute cumulative sum of lap time seconds
    valid_laps['cumulative_lap_time'] = valid_laps.groupby('Driver')['LapTime'].cumsum()

    # Check cumulative time should increase monotonically per driver
    is_monotonic_inc = valid_laps.groupby('Driver')['cumulative_lap_time'].diff().dropna().ge(0).all()

    if is_monotonic_inc:
        print('All Driver Cumulative Lap Times Monotonically Increasing')
    else:
        print('Non-increasing Cumulative Lap Times')
        diffs = valid_laps.groupby('Driver')['cumulative_lap_time'].diff()
        non_monotonic_mask = diffs < 0
        print(valid_laps[non_monotonic_mask][['Driver', 'LapNumber', 'LapTime', 'cumulative_lap_time']])

if __name__ == '__main__':
    main()