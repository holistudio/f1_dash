import os
import sys
import logging
import fastf1
import pandas as pd

# Configure cache relative to this script to ensure it works from any CWD
script_dir = os.path.dirname(os.path.abspath(__file__))
cache_path = os.path.join(script_dir, '../data/cache')
fastf1.Cache.enable_cache(cache_path)

class MaxLevelFilter(logging.Filter):
    """Filter to allow records up to a specific level."""
    def __init__(self, max_level):
        super().__init__()
        self.max_level = max_level

    def filter(self, record):
        return record.levelno <= self.max_level

def setup_logging():
    """Configures logging to send INFO to stdout and WARNING/ERROR to stderr."""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Stdout Handler (INFO and below)
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.INFO)
    stdout_handler.addFilter(MaxLevelFilter(logging.INFO))
    stdout_handler.setFormatter(formatter)

    # Stderr Handler (WARNING and above)
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.WARNING)
    stderr_handler.setFormatter(formatter)

    logger.addHandler(stdout_handler)
    logger.addHandler(stderr_handler)

def main():
    setup_logging()

    # Load race session
    session = fastf1.get_session(year=2019, gp='Hungary', identifier='R')
    session.load()

    # Access Laps DataFrame
    laps = session.laps

    # Inspect columns
    logging.info(f'Lap Data Columns: {laps.columns}')

    # Inspect row count
    logging.info(f'Number of rows: {len(laps)}')

    # Get list of drivers
    drivers = laps['Driver'].unique()
    logging.info(f'Drivers: {drivers}')

    # Convert `LapTime` from Timedelta to float seconds
    laps['LapTime'] = laps['LapTime'].dt.total_seconds()

    # Check for NaT values in LapTime
    if laps['LapTime'].isna().any():
        n_nat = laps['LapTime'].isna().sum()
        logging.warning(f'Number of NaT Lap Times: {n_nat}')
    else:
        logging.info('All Lap Times non-NaT')
        column_dtype = laps['LapTime'].dtype
        logging.info(f'dtype: {column_dtype}')

    # Drop rows with NaT LapTimes
    # Use .copy() to avoid SettingWithCopyWarning
    valid_laps = laps[laps['LapTime'].notna()].copy()

    # Group by `Driver` and compute cumulative sum of lap time seconds
    valid_laps['cumulative_lap_time'] = valid_laps.groupby('Driver')['LapTime'].cumsum()

    # Check cumulative time should increase monotonically per driver
    is_monotonic_inc = valid_laps.groupby('Driver')['cumulative_lap_time'].diff().dropna().ge(0).all()

    if is_monotonic_inc:
        logging.info('All Driver Cumulative Lap Times Monotonically Increasing')
    else:
        logging.warning('Non-increasing Cumulative Lap Times')
        diffs = valid_laps.groupby('Driver')['cumulative_lap_time'].diff()
        non_monotonic_mask = diffs < 0
        logging.warning(f"Details:\n{valid_laps[non_monotonic_mask][['Driver', 'LapNumber', 'LapTime', 'cumulative_lap_time']]}")

    # Create in-lap and out-lap flags
    valid_laps['is_inlap'] = valid_laps['PitInTime'].notna()
    valid_laps['is_outlap'] = valid_laps['PitOutTime'].notna()
    valid_laps['is_pit_lap'] = valid_laps['is_inlap'] | valid_laps['is_outlap']

    # Compute pit_stop_number
    valid_laps['pit_stop_number'] = valid_laps.groupby('Driver')['is_inlap'].cumsum().astype(int)

    # Verify: Stint should increment by 1 after each is_inlap == True
    # We compare current Stint with next lap's Stint for in-laps
    valid_laps['next_stint'] = valid_laps.groupby('Driver')['Stint'].shift(-1)
    in_laps_check = valid_laps[valid_laps['is_inlap'] & valid_laps['next_stint'].notna()]
    mismatches = in_laps_check[in_laps_check['next_stint'] != in_laps_check['Stint'] + 1]

    if not mismatches.empty:
        logging.warning(f"Stint consistency check failed for {len(mismatches)} laps.")
        logging.warning(f"Details:\n{mismatches[['Driver', 'LapNumber', 'Stint', 'next_stint']]}")
    else:
        logging.info("Stint consistency verified: Stint increments after each in-lap.")

    valid_laps.drop(columns=['next_stint'], inplace=True)

if __name__ == '__main__':
    main()