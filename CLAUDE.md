# F1 Pit Stop Delta Analysis

## Project Overview
Python data pipeline + Tableau dashboard for post-race pit stop analysis. Computes time lost to pit stops and recovery rates against a reference driver.

## Key Constraints and Limitations

- Do NOT: Provide code changes beyond what I ask for. This is a learn-to-code project.
- Always assist in my learning by writing code comments explaining the code lines you write.

## Environment
- Windows 10 with WSL (Ubuntu)
- Project lives on Windows filesystem, accessed via WSL at `/mnt/c/`
- Anaconda for environment management
- `uv` for package installation within conda env
- Tableau Desktop/Public on Windows

## Tech Stack
- Python 3.11+
- FastF1 library for F1 timing data
- pandas for data transformation
- Tableau for visualization

## Commands
```bash
# Navigate to project (adjust path as needed)
cd /mnt/c/Users/<username>/Projects/f1-pitstop-analysis

# Environment setup (run once)
conda create -n f1analysis python=3.11 -y
conda activate f1analysis
pip install uv

# Package installation
uv pip install fastf1 pandas

# Data pipeline
python src/extract.py <year> <race> <session>
python src/transform.py
python src/validate.py
```

## File Paths
- WSL sees project at: `/mnt/c/Users/<username>/Projects/f1-pitstop-analysis/`
- Windows sees project at: `C:\Users\<username>\Projects\f1-pitstop-analysis\`
- Tableau connects to: `C:\Users\<username>\Projects\f1-pitstop-analysis\data\processed\`
- Same files, no path translation needed for Tableau

## Project Structure
```
/assets           - media, static files, research notes
/src              - Python scripts, notebooks (extract, transform, validate)
/data/raw         - Raw FastF1 exports
/data/processed   - Tableau-ready CSVs
/data/cache       - FastF1 cache directory
/tableau          - .twb/.twbx workbook files
/docs             - PRD, data dictionary
```

## File Boundaries
- Safe to edit: `/src/`, `/docs/`, `/tableau/`
- Never touch: Conda env dirs, `/__pycache__/`, `/data/raw/` (treat as immutable)

## Coding Rules
- Convert all `pandas.Timedelta` to float seconds before CSV export
- Use `pd.notna()` not `!= NaT` for null checks on timedeltas
- Prefix derived columns with `calc_` (e.g., `calc_cumulative_time`)
- Boolean flags use `is_` prefix (e.g., `is_inlap`, `is_outlap`)
- Use `pick_drivers` and `pick_teams` and never use `pick_driver` and `pick_team` (future deprecated functions)
- Print warnings to stderr, data to stdout

## Data Conventions
- One row = one lap for one driver
- `LapNumber` is the join key for gap calculations
- Positive gap = analysis driver behind reference
- Negative gap = analysis driver ahead

## Known FastF1 Quirks
- `Time` column = session time at lap completion, not lap duration
- `PitInTime` present = this lap is an inlap
- `PitOutTime` present = this lap is an outlap
- `Stint` increments after each pit stop
- Lap 1 often has incomplete data; handle gracefully
- Some drivers may have fewer laps (retirement/lapping)
- Enable cache to avoid re-downloading: `fastf1.Cache.enable_cache('data/cache')`

## Validation Checks (must pass before export)
- No duplicate (Driver, LapNumber) pairs
- All `calc_` columns are float, not timedelta
- Retired drivers flagged in `is_retired` column
- Lapped drivers flagged in `is_lapped` column

## Common Issues
- If `uv pip install` fails, ensure conda env is activated first
- If FastF1 hangs, check internet connection (it downloads from F1 API)
- Slow file I/O on `/mnt/c/` is normal; WSL accessing Windows filesystem has overhead

## Reference Docs
- FastF1 Laps: https://docs.fastf1.dev/core.html#fastf1.core.Laps
- FastF1 Time Explanation: https://docs.fastf1.dev/time_explanation.html
- Tableau LOD Expressions: https://help.tableau.com/current/pro/desktop/en-us/calculations_calculatedfields_lod.htm
