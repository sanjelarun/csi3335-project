# CSI3335 Group Project - Immaculate Party Time

This is the CSI 3335 Group Project for team **Immaculate Party Time**.
Members:
- August Rothpletz
- Logan Rigdon
- Mitchell Thompson
- Samuel Fries


## Web App
The core of this project is a web app that shows a team roster and solves the immaculate grid.
To start the app:
1. Set up your python virtal environment
2. Start your virtual environment
3. Run `pip install -r config\requirements.txt`
4. Add the database user the app uses
    a. Start an instance of MySQL in your terminal: `mysql -u root -p`
    b. Add the user: `\. config\addUser.sql`
    c. exit mysql: `exit`
5. Update the database (see below)
6. Start the app: `flask run`

The app should now be started and can be found at [http://localhost:5000](http://localhost:5000)!

## Database Update

We have added significant changes to the database, adding the 2023 data and some other data used in the web app.

### Steps to Update Database

To update the databse to have the needed extra data in order to run the run the app, as well as to update the database with 2023 player data:
1. Configure the project's setup by following steps 1-4 in the section above
2. Run `python Update_Database/UpdateDatabase.py`

The project should now be fully updated with 2023 data and the info needed to run the app!

### Things we updated
- Added all data from the 2023 Baseball Season in the Lahman Database.
- Updated Players to add any death locations and dates since last update.
- Added awards that were missing from Lahman 2022.
- Created a "Seasons" table containing statistics about a seaon for the MLB as a whole
   - wOBA stats Pulled from the [Fan Graphs 'Guts!' page](https://www.fangraphs.com/guts.aspx).
   - Season Totals pulled from Baseball Reference.
   - Used to get season constants and totals used to calculate FIP and WAR values.