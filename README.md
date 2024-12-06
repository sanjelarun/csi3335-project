# CSI3335 Group Project - Immaculate Party Time

This is the CSI 3335 Group Project for team **Immaculate Party Time**.
Members:
- August Rothpletz
- Logan Rigdon
- Mitchell Thompson
- Samuel Fries

## Config 
To run the app, some configuration is required:

1. Set up your python virtal environment
2. Start your virtual environment
3. Run `pip install -r config\requirements.txt`
4. Add the database user the app uses
    a. Start an instance of MySQL in your terminal: `mysql -u root -p`
    b. Add the user: `\. config\addUser.sql`
    c. exit mysql: `exit`
5. Update the database (see below)

** If you want to change what database, port, etc. the app uses: **
Update the connection used in `csi3335f2024.py`

## Web App
The core of this project is a web app that shows a team roster and solves the immaculate grid.
To start the app:
1. Set up the project configuration (see the config section)
2. Update the database (see below)
3. Start the app: `flask run`

### Login
You can create your own account, or log into the admin account using the following credentials:
username: admin
password: password

The app should now be started and can be found at [http://localhost:5000](http://localhost:5000)!

## Database Update

We have added significant changes to the database, adding the 2023 data and some other data used in the web app.

### Steps to Update Database

To update the databse to have the needed extra data in order to run the run the app, as well as to update the database with 2023 player data:
1. Set up the project configuration (see the config section)
2. Run `UpdateDatabase.py`

The project should now be fully updated with 2023 data and the info needed to run the app!

### Things we updated
- Added all data from the 2023 Baseball Season in the Lahman Database.
- Updated Players to add any death locations and dates since last update.
- Added awards that were missing from Lahman 2022.
- Created a "Seasons" table containing statistics about a seaon for the MLB as a whole
   - wOBA stats Pulled from the [Fan Graphs 'Guts!' page](https://www.fangraphs.com/guts.aspx).
   - Season Totals pulled from Baseball Reference.
   - Used to get season constants and totals used to calculate FIP and WAR values.


## Cool things we did

Here is a (non-comprehensive) list of a features we added beyond the project requirements. We think they're pretty cool, though I suppose that's for you to decide.
1. **Dynamic Fields**. When you select a year for the team roster, the `team` page will only have teams that were actively in the MLB that year.
2. **Season Data**. We added a full new **Seasons** table that contains some overall statistics about a year as a whole for the entire MLB.
3. **CSS Depth Chart Diamond**. We have a great looking baseball diamond for displaying our depth chart, just like on Fangraphs. It's not an image, its _all CSS._
4. **WAR and other calculated stats**. Our tables display many derived statistics that are all calculated at runtime, including WAR. Other teams were too scared to take on the challenge of calculating war, deciding to webscrape it from Baseball Reference and storing it in their database. However, we took the time to figure out how to calculate it ourselves.
5. **No Manual Question Entry**. Our immaculate grid solver webscrapes the questions from any official Immaculate Grid problem when you paste in its URL, so you don't have to manually type in every question.
6. **Optimized Immaculate Grid**. We have, not one, but _TWO_ ways to solve the immaculate grid.
   1. The first method makes some API requests to ImmaculateGrid.com's backend to _always_ fetch the most rare answer!
   2. The second method determines an answer from our database, as originally intended.
7. **Links to baseball-reference**. Our roster embeds a link for each player to their [Baseball Reference](https://www.baseball-reference.com/players/) Page, where a user can learn more about them in the context of their entire career.
8. **Syling**. We think our web app looks great!