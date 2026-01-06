import os
import sys
import logging
import fastf1

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

if __name__ == '__main__':
    main()