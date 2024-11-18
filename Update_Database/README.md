# Immaculate Party Time - Update Database.

The following contains everything needed to update the database to have the most recent MLB statistics contained in the publicly availible Lahman MLB database.

## To update your database:
1. From the project root, run `cd Update_Database` to change to this directory.
2. Ensure your MySQL server is running, and that the credentials are contained in the file `csi3335f2024.py`.
2. Run `python UpdateDatabase.py` in your terminal to update the database.

## Things we updated
- Added all data from the 2023 Baseball Season in the Lahman Database.
- Updated Players to add any death locations and dates since last update
- Added awards that were missing from Lahman 2022
- Created a "Seasons" table containing statistics about a seaon for the MLB as a whole
   - Pulled from the [Fan Graphs Guts! page](https://www.fangraphs.com/guts.aspx)
   - Primarily used to get the FIP constant for the year, to calculate FIP and WAR values