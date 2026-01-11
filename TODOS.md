# TODOs

## Part A: Data Preparation

### 1. Load a single race session using FastF1
- [x] Import fastf1 and enable cache (`fastf1.Cache.enable_cache('data/cache')`)
- [x] Use `fastf1.get_session(year, race_name, 'R')` to get a race session
- [x] Call `session.load()` to fetch timing data
- [x] Access lap data via `session.laps`
- [x] Inspect columns with `session.laps.columns` and row count with `len(session.laps)`
- [x] Get list of drivers with `session.laps['Driver'].unique()`

### 2. Compute cumulative race time for each driver
- [x] Convert `LapTime` from Timedelta to float seconds using `.dt.total_seconds()`
- [x] Check for NaT values in `LapTime`
- [x] Group by `Driver` and compute cumulative sum of lap time seconds
- [x] Store result in new column `cumulative_lap_time`
- [x] Verify: cumulative time should increase monotonically per driver
- [x] Handle NaT values in `LapTime` (decide: drop, fill with 0, or interpolate)
- [x] Drop since dashboard is for pit stop loss relative to appropriate pairs of analysis and reference drivers. Invalid LapTime should not get visualized in the first place.

#### Revisit later
- [ ] Automatically verify clean data in `validate.py` file.
- [ ] Warnings should go to stderr

### 3. Create in-lap and out-lap flags
- [ ] Create `is_inlap` column: `pd.notna(laps['PitInTime'])`
- [ ] Create `is_outlap` column: `pd.notna(laps['PitOutTime'])`
- [ ] Create `is_pit_lap` column: `is_inlap | is_outlap`
- [ ] Compute `pit_stop_number` as cumulative count of `is_inlap` per driver
- [ ] Verify: `Stint` should increment by 1 after each `is_inlap == True`

### 4. Build a retirement/lapping detection check that prints warnings
- [ ] Find race winner's max `LapNumber` (driver with Position == 1 on final lap)
- [ ] For each driver, compare their max `LapNumber` to winner's
- [ ] Flag `is_retired`: driver's max lap < winner's max lap - 1
- [ ] Flag `is_lapped`: driver's max lap < winner's max lap (but finished race)
- [ ] Print warning to stderr for each retired driver with their last lap number
- [ ] Print warning to stderr for each lapped driver with lap deficit
- [ ] Add `is_retired` and `is_lapped` boolean columns to dataframe

### 5. Export to CSV with all necessary columns, lap times in seconds
- [ ] Select final column set (see PRD Section 6.3 for schema)
- [ ] Convert any remaining Timedelta columns to float seconds
- [ ] Verify no Timedelta dtypes remain: `df.select_dtypes(include=['timedelta64'])`
- [ ] Check for duplicate `(Driver, LapNumber)` pairs
- [ ] Export to `data/processed/laps_final.csv` with `index=False`
- [ ] Verify CSV is readable: reopen with pandas and spot-check values

---

## Part B: Tableau Build

- [x] Add `Driver Status` field that categorizes each driver as "Full Race", "Retired", or "Lapped"

### 1. Create driver selection parameters
- [x] Create Parameter: `Analysis Driver` (String, list of all drivers from data)
- [x] Create Parameter: `Reference Driver` (String, list of all drivers from data)
- [x] Set default values (e.g., race winner as reference, P2 as analysis driver)

### 2. Build a calculated field for gap-to-reference using LOD expressions
- [x] Create calculated field `Reference Cumulative Time`:
      `{ FIXED [LapNumber]: MAX(IF [Driver] = [Reference Driver] THEN [calc_cumulative_time_sec] END) }`
- [x] Create calculated field `Gap to Reference`:
      `IF [Driver] = [Analysis Driver] THEN [calc_cumulative_time_sec] - [Reference Cumulative Time] END`
- [x] Verify: positive values = analysis driver behind, negative = ahead

### 3. Construct Plot One: Gap-to-Reference Evolution
- [x] Create new worksheet "Gap Evolution"
- [x] Drag `LapNumber` to Columns (continuous)
- [x] Drag `Gap to Reference` to Rows
- [x] Filter to `[Driver] = [Analysis Driver]`
- [x] Set mark type to Line
- [x] Add secondary axis or layer for pit stop markers
- [x] Mark points where `is_pit_lap = True` for analysis driver (distinct shape/color)
- [x] Mark points where reference driver pitted (use LOD to find those laps)
- [x] Add annotations or labels for pit stop numbers
- [x] Format axis: Y-axis label "Gap (seconds)", reference line at 0

- [x] Show every Lap Number not every other Lap Number

### 4. Construct Plot Two: Lap Time Comparison
- [x] Create new worksheet "Lap Time Comparison"
- [x] Drag `LapNumber` to Columns (continuous)
- [x] Drag `calc_lap_time_sec` to Rows
- [x] Drag `Driver` to Color
- [x] Filter to show only `[Analysis Driver]` and `[Reference Driver]`
- [x] Add filter: exclude `is_pit_lap = True`
- [x] Set mark type to Line (or Line + Circle)
- [ ] Add `Compound` to shape or color detail for tire visibility
- [x] Format Y-axis to appropriate scale (likely 60-120 seconds range)
- [x] Add tooltip: Lap, Time, Compound, TyreLife, Position
- [x] Show every Lap Number not every other Lap Number

### 5. Add interactivity so both plots update when driver selections change
- [x] Show both parameter controls on dashboard
- [x] Verify Plot One updates when either parameter changes
- [x] Verify Plot Two filters update when parameters change
- [x] Add action: hover on Plot One highlights corresponding lap in Plot Two
- [x] Test edge case: select a retired driver (should show partial data)
- [x] Test edge case: select same driver for both parameters (should show flat zero line)
- [x] Add warning text field that displays if selected driver is retired/lapped
- [x] Move "Lap Number" to bottom of the chart
- [ ] Visual style/color palette matching F1 dashboards