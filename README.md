# f1_dash 🏎️

A dashboard for analyzing pit stop strategy in Formula 1 racing sessions. This project serves as a learning exercise for using Tableau to make interactive self-serve dashboards.

<img src="assets/0_full_dashboard.png">

Interactive dashboard online at: https://public.tableau.com/app/profile/daniel.lu8478/viz/Formula1RacingPitStopGapRecoveryData/PitStopAnalysisDashboard

## Data Visualizations

The dashboard is configured to compare gaps between and lap times of two drivers, analysis driver and reference driver.

- **Analysis Driver-to-Reference Gap Evolution**: Plot shows gap between drivers at the end of each lap. Negative gap means analysis driver is ahead of reference driver.
- **Analysis vs Reference Driver Lap Times**: Plot shows lap times for each driver.
- **Tire Compound**: Supplemental chart showing tire compound used by each driver during every lap.

## Usage

| Step |  Menu |
|:------|----:|
| 1. The user selects analysis and reference driver on the dropdown menus on the top right. Both plots will update to show the corresponding driver delta, lap times, and tire compounds.|  <img src="assets/1_menu.png" width="300 px"> |
| 2. The user can also zoom in/out by specifying the min and max lap numbers  |  <img src="assets/2_lap.png" width="300 px"> |  
| 3. A warning will be displayed if any issues were encountered during the racing session that may cause misleading values in the data (e.g., driver retired early or analysis driver lapped reference driver)  |  <img src="assets/3_driver_warning.png" width="300 px"> |  

## Case Study

A demo of this dashboard looks at Lewis Hamilton's victory of Max Verstappen in the 2019 Hungarian Grand Prix.

Hamilton starts the race at P3 behind Verstappen in P1 and gets to P2 by the end of Lap 1. At Lap 25, Verstappen undercuts with an early pit stop and regains P1 during Hamilton's pit stop.

<img src="assets/01_lap25.png">


At Lap 48, Hamilton makes another pit stop. Hamilton's team had not planned for two pit stops before the race but decided that a switch back to medium tires would help close the gap.

<img src="assets/02_lap48.png">

By Lap 66, Hamilton had closed the gap, forcing Verstappen to stay out on hard tires.

Hamilton's second pit stop was also considered a "free pit stop" due to his significant 40s gap with Charles LeClerc behind him, resulting in no loss in racing position.

<img src="assets/03_lap48_lec.png">