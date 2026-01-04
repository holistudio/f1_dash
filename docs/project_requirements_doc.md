# Project Requirements Document: F1 Pit Stop Delta Analysis Dashboard

**Version:** 1.0  
**Last Updated:** January 2026  
**Author:** [holistudio](https://github.com/holistudio)  
**Status:** Draft

---

## 1. Executive Summary

### 1.1 Purpose
Build a post-race debrief dashboard that answers: *What was the actual time cost of each pit stop, and how long did it take to recover?*

### 1.2 Scope
Single-race analysis tool. Given a completed F1 race session, compute the time delta between a selected driver and a reference competitor, visualize pit stop impacts, and show lap time degradation patterns.

### 1.3 Success Criteria
- User can select any two drivers from a race
- Gap evolution chart clearly shows pit stop time loss and recovery slope
- Lap time chart reveals tire degradation patterns per stint
- Data pipeline runs without manual intervention once race/year specified

---

## 2. Problem Statement

### 2.1 User Need
After a race, analysts want to understand whether pit stop timing was optimal. This requires comparing a driver's cumulative race time against a reference (ideally someone who stayed out or ran a different strategy) and measuring:
1. Instantaneous time lost when pitting
2. Rate of time recovery on fresh tires
3. Whether recovery was complete before the next strategic event

### 2.2 Current Gap
Raw F1 timing data provides lap times but not:
- Cumulative elapsed time per driver
- Gap-to-reference calculations
- Explicit in-lap/out-lap flags for filtering
- Warnings about retired or lapped drivers

---

## 3. Data Source Specification

### 3.1 Primary Data Source
**FastF1 Python Library** (https://docs.fastf1.dev)

### 3.2 Data Retrieval
```
Session = fastf1.get_session(year, race_name, 'R')
Session.load()
laps = Session.laps
```

### 3.3 Available Raw Columns
| Column | Type | Description |
|--------|------|-------------|
| Time | Timedelta | Session time at lap completion |
| Driver | str | Three-letter abbreviation (e.g., VER, HAM) |
| DriverNumber | str | Car number |
| LapTime | Timedelta | Duration of this lap |
| LapNumber | float | Lap count (1, 2, 3...) |
| Stint | float | Tire stint number (increments after pit) |
| PitOutTime | Timedelta | Session time exiting pit (NaT if not outlap) |
| PitInTime | Timedelta | Session time entering pit (NaT if not inlap) |
| Sector1Time | Timedelta | Sector 1 duration |
| Sector2Time | Timedelta | Sector 2 duration |
| Sector3Time | Timedelta | Sector 3 duration |
| Compound | str | Tire compound (SOFT, MEDIUM, HARD, INTERMEDIATE, WET) |
| TyreLife | float | Laps on current tire set |
| FreshTyre | bool | True if tire was new at stint start |
| Position | float | Race position at lap completion |
| Team | str | Constructor name |
| IsAccurate | bool | FastF1's data quality flag |
| TrackStatus | str | Yellow flag, safety car indicators |

### 3.4 Data Limitations
- Lap 1 timing often incomplete or anomalous
- Retired drivers have fewer rows (last lap is their final entry)
- Lapped drivers complete fewer laps than leader
- `Time` column name is misleading (it's session timestamp, not duration)

---

## 4. Derived Data Requirements

### 4.1 Computed Columns (Python)

| Column | Formula | Purpose |
|--------|---------|---------|
| `calc_lap_time_sec` | `LapTime.total_seconds()` | Tableau-compatible numeric |
| `calc_cumulative_time_sec` | Running sum of `LapTime` per driver | Gap calculation basis |
| `is_inlap` | `pd.notna(PitInTime)` | Filter/mark pit entry laps |
| `is_outlap` | `pd.notna(PitOutTime)` | Filter/mark pit exit laps |
| `is_pit_lap` | `is_inlap OR is_outlap` | Combined pit activity flag |
| `pit_stop_number` | Cumulative count of `is_inlap` per driver | Label pit stops (1st, 2nd, etc.) |

### 4.2 Validation Flags (Python)

| Flag | Condition | Action |
|------|-----------|--------|
| `is_retired` | Driver's max `LapNumber` < race winner's max `LapNumber` - 1 | Warn user in export log |
| `is_lapped` | Driver's max `LapNumber` < reference driver's max `LapNumber` | Warn user, handle null gaps |
| `has_incomplete_data` | `IsAccurate == False` on any lap | Flag for user awareness |

### 4.3 Gap Calculation (Tableau or Python)

**Formula:**  
`gap_to_reference = calc_cumulative_time_sec[analysis_driver] - calc_cumulative_time_sec[reference_driver]`

**Join Key:** `LapNumber`

**Sign Convention:**
- Positive = analysis driver is behind (slower cumulative time)
- Negative = analysis driver is ahead

---

## 5. Visualization Specifications

### 5.1 Plot One: Gap-to-Reference Evolution

**Purpose:** Show instantaneous pit stop time loss and recovery trajectory.

| Element | Specification |
|---------|--------------|
| Chart Type | Line chart |
| X-Axis | `LapNumber` (continuous, 1 to race end) |
| Y-Axis | `gap_to_reference` (seconds) |
| Line | Gap value per lap for selected analysis driver |
| Markers | Distinct points at laps where `is_pit_lap == True` for either driver |
| Annotation | Label pit stops with driver abbreviation + stop number |

**Visual Interpretation Guide:**
- Upward spike = time lost (e.g., pit stop)
- Downward slope after spike = recovery on fresh tires
- Flat line = no net gain/loss
- Slope magnitude = recovery rate (seconds per lap)

### 5.2 Plot Two: Lap Time Comparison

**Purpose:** Compare raw pace and tire degradation between two drivers.

| Element | Specification |
|---------|--------------|
| Chart Type | Dual-line chart |
| X-Axis | `LapNumber` (continuous) |
| Y-Axis | `calc_lap_time_sec` (seconds) |
| Lines | One per driver (analysis + reference), distinct colors |
| Filter | Exclude rows where `is_pit_lap == True` |
| Markers | Optional: mark stint boundaries or compound changes |

**Visual Interpretation Guide:**
- Fresh tires show initial drop then gradual rise (degradation)
- Crossing lines indicate pace crossover
- Steeper slope = faster degradation
- Vertical discontinuities at stint changes (filtered out-laps reconnect)

### 5.3 Interactivity Requirements

| Feature | Implementation |
|---------|---------------|
| Analysis Driver Selector | Tableau Parameter → dropdown of all drivers |
| Reference Driver Selector | Tableau Parameter → dropdown of all drivers |
| Dynamic Gap Calculation | LOD expression using parameter values |
| Tooltip | Lap number, gap value, compound, tire life, position |
| Linked Highlighting | Hovering on Plot One highlights corresponding lap in Plot Two |

---

## 6. Technical Implementation

### 6.1 Python Pipeline Architecture

```
src/
├── extract.py      # Load FastF1 session, export raw laps
├── transform.py    # Compute derived columns, validate
├── validate.py     # Quality checks, retirement/lapping detection
└── config.py       # Race selection parameters
```

### 6.2 Data Flow

```
FastF1 API → extract.py → data/raw/laps_raw.csv
                              ↓
                        transform.py
                              ↓
                   data/processed/laps_final.csv
                              ↓
                    Tableau Data Source
                              ↓
                    Dashboard (2 worksheets)
```

### 6.3 Export Schema

Final CSV columns for Tableau:

| Column | Type | Notes |
|--------|------|-------|
| LapNumber | int | Join key |
| Driver | str | Filter/parameter match |
| Team | str | Color encoding |
| calc_lap_time_sec | float | Y-axis Plot Two |
| calc_cumulative_time_sec | float | Gap calculation input |
| Stint | int | Grouping |
| Compound | str | Color/shape encoding |
| TyreLife | int | Tooltip |
| Position | int | Tooltip |
| is_inlap | bool | Filter |
| is_outlap | bool | Filter |
| is_pit_lap | bool | Marker condition |
| pit_stop_number | int | Annotation |
| is_retired | bool | Warning indicator |
| is_lapped | bool | Warning indicator |

---

## 7. Edge Cases and Error Handling

### 7.1 Retired Drivers
- **Detection:** Compare driver's max lap to winner's lap count
- **Handling:** Include in dropdown but show warning icon; gap calculation returns null after retirement lap

### 7.2 Lapped Drivers
- **Detection:** Driver completes fewer laps than reference at race end
- **Handling:** Gap calculation only possible for overlapping lap numbers; show "(lapped)" annotation

### 7.3 Safety Car / Red Flag
- **Detection:** `TrackStatus` column indicates neutralized racing
- **Handling:** Optional: mark these periods on charts; lap times during SC are not representative

### 7.4 Missing Data
- **Detection:** `IsAccurate == False` or null `LapTime`
- **Handling:** Exclude from calculations; show data quality warning in dashboard

---

## 8. User Stories

### 8.1 Primary User Story
> As a race analyst, I want to select any driver and compare their gap evolution against a reference driver so that I can quantify pit stop time costs and recovery rates.

### 8.2 Secondary User Stories
> As a race analyst, I want to filter out in-laps and out-laps from pace charts so that artificially slow laps don't compress my visualization scale.

> As a race analyst, I want to see pit stops marked directly on the gap chart so that I can immediately identify which strategic events caused gap changes.

> As a race analyst, I want to be warned if a driver retired or was lapped so that I understand why their data may be incomplete.

---

## 9. Acceptance Criteria

### 9.1 Data Pipeline
- [ ] Extract script successfully loads any 2020+ race session
- [ ] All timedelta columns converted to float seconds
- [ ] In-lap and out-lap flags correctly identify pit activity
- [ ] Retired drivers flagged with warning message in console
- [ ] Lapped drivers flagged with warning message in console
- [ ] Output CSV has no duplicate (Driver, LapNumber) pairs

### 9.2 Tableau Dashboard
- [ ] Both driver selectors populate with all drivers from race
- [ ] Gap chart updates dynamically when either parameter changes
- [ ] Lap time chart excludes pit laps by default
- [ ] Pit stops visually marked on gap chart
- [ ] Tooltips show lap number, gap, compound, tire life
- [ ] Charts render in under 3 seconds on standard hardware

---

## 10. Future Enhancements (Out of Scope)

- Multi-race comparison across a season
- Predictive pit window optimization
- Integration with weather data for wet race analysis
- Automated "optimal reference driver" selection
- Export to PowerBI as alternative to Tableau

---

## 11. References

- FastF1 Documentation: https://docs.fastf1.dev
- FastF1 Laps Reference: https://docs.fastf1.dev/core.html#fastf1.core.Laps
- FastF1 Time Explanation: https://docs.fastf1.dev/time_explanation.html
- Tableau LOD Expressions: https://help.tableau.com/current/pro/desktop/en-us/calculations_calculatedfields_lod.htm
- Tableau Parameters: https://help.tableau.com/current/pro/desktop/en-us/parameters.htm

---

## 12. Glossary

| Term | Definition |
|------|------------|
| Inlap | The lap on which a driver enters the pit lane |
| Outlap | The lap on which a driver exits the pit lane (first lap on new tires) |
| Stint | A continuous sequence of laps on the same set of tires |
| Gap | Time difference between two drivers' cumulative race times |
| Undercut | Pitting earlier than a competitor to gain track position via fresh tire pace |
| Overcut | Staying out longer than a competitor, gambling on track position or tire strategy |
| Degradation | Gradual loss of tire performance over a stint, visible as increasing lap times |
| Recovery | The process of regaining lost time after a pit stop through faster lap times |
