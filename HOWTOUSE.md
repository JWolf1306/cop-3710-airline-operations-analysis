# How to Use this Repository
## Step 1: Run create_db.sql
Open up Oracle FreeSQL and run the create_db.sql file provided in the repository. Remember to delete all tables within your worksheet before running the file to prevent any interference.
## Step 2: Download the data ZIP
Download the data ZIP file provided in the repository, which contains the raw data used for this project. Unzip the file and be sure to check the path for each file as it will be needed for steps 3 and 4.
## Step 3: Run preprocess.py
Before running this file, you must update the paths to the raw data files. There is also the option to name the folder where the processed data will be stored. 

The lines to update paths to data are as follows:

(OPTIONAL) Name of processed data folder: Line 4

AIRLINE: Line 23

AIRPORT: Line 39

AIRCRAFT: Line 58

ROUTE: Line 66

FLIGHT: Line 82

FLIGHT_DELAY: Line 127

## Step 4: Run dataload.py
This file requires you to update the file paths for the processed data. However, this file only uses a general path to the folder so the files can be accessed when needed.
This file also requires you to enter your database credentials so the data can be loaded into the tables.
Your database information can be accessed by clicking "Connect To The Database" on Oracle FreeSQL, which will bring up your credentials. You must also have the path to your Oracle client; if you do not have an Oracle client installed,
they can be downloaded from Oracle's website.

The line to enter the path to your Oracle client is line 6.

The lines to update your database credentials are from lines 7 to 9.

The lines to update the general path to the processed data is line 14.

## Step 5: Run app.py
Similar to step 4, this file requires you to update the database credentials so the file can connect to your Oracle database. Once your credentials have been entered, you will be able to use the app.

The lines to update your database credentials are from lines 4 to 6.
