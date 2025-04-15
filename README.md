# Core assessment outline
The main requirement is to process two data files using snowflake, and present some analysis on these data files using streamlit. 
The data files are joined by a foreign key, there is also a single 'config file', which we will think of as a static reference table for the most part. 
The two data files should be treated as if they would be subject to a daily load, so probably best to handle them using SCD 2 or similar. 

The app should be treated as though it were to be used for internal reporting, and the final transformed data to be shared externally,
so we'll apply our business logic in the final stage of the pipeline, as opposed to in the dashboard itself. This way the shared data can be identical to that used
for analytics. This will also mean our dashboards compute can be solely focused on graphics. 

The app will also be subject to a biweekly release cycle, so allow for easy change management. 

## Data processing features
 - DDL for all database objects, ie. tables, schemas, database, and any stored procedures or functions. 
 - (infrastructure as code is probably not necessary for this minimal example, but we'll point out where we might include such workflows)
 - procedures for ingesting raw data, and applying any transformations. 
 - a basic logging library, we can either write out log files to a local file, or if time permits have a seperate streamlit app to mock up a 'cloudwatch'-esque monitoring service
 - at least 90% unit test coverage, and some minimal pipeline tests. A 5 line test dataset for the final target table is plenty, this is mainly to demonstrate the 
   test infrastructure. 

## Streamlit dashboard features
This will likely have to wait until we have a better understanding of the data, but let's just have fun with some of streamlits more interesting features, thinking fragments, 
interactive plotly elements, lottie elements, styleable containers, that sort of thing. It's going to be very minimal analysis so we'll focus on UI/UX and making everything look 
as slick as possible. A few things we could add would be 
 - data caching
 - a seperate page for logging and monitoring
 - a seperate page for the excel download, include a sample of the data before download. 
 - Potentially a seperate page for updating the static config data files (time permitting)

## Testing and an outline for CI/CD
  - pytest for any python tests
  - st.testing for UI validation
  - data validation, use pydantic to ensure the raw data is compliant, use a small test dataset to ensure the pipeline runs correctly
  - CI/CD could do some of the following (very unlikely to include this in this MVP):
    * Run linting and tests as part of pre commit hooks or CI
    * Deploy the streamlit app itself
    * Update database objects via terraform or similar

## Sugar on top
Depending on how/if we decide to host the streamlit app, or if we just run it locally, we could set up a refresh trigger to read updated data into the streamlit app. If we host
within snowflake we wont be able to read any external triggers as snowflake hosted streamlit apps are sandboxed, but if we host it on streamlit cloud (or on the optiplex server) 
we could have proper file arrival triggers. Either way, a nice touch would also be to have a "Data last updated at: <timestamp>" displayed in the top of the app. 



## Orchestration
 - a file gets dropped in a local directory, which simulates a file being updated in verity
 - a script watching this directory reads this update, and pushes this file to snowflake using a copy into, or snowflake-connector-python
 - the pipeline runs and it's metadata and run statistics are written to some additional metadata table
 - the streamlit app polls this metadata table every x seconds/minutes etc. or on a button click, and updates the data on an update


## First steps
Set up a watcher method that triggers a function when a local directory gets updated, this will become the pipeline trigger script

## Update
Watcher runs, and gives clean colour coded output. Also added debouncing to ignore create and modify events on the same file. 
Streamlit app mocked up on sample data. 4 pages, added some css into a styling library to use a similar colour theme to the core website. 

## Next steps
 - Create a snowflake trial account.
 - Work out how to run against this trial account with the snowflake connector.
 - Create a table from a python instance. 
 - Write up DDLs for the two data tables and the one static reference table.
 - Write an 'iac' lib that runs these DDLs (would be done with terraform in a real project).
 - Write a procedure which loads the sample data into the created RAW tables. 
 - Write a procedure which triggers when the above proc runs successfully which loads a TRF 
   table using SCD 2. 
 - Write a task which orchestrates the above two procedures and will act as the entry point
   for the job. 
 - Write a logging library for all the above procedures to use. 
 - Write tests for the above procedures and generate a sample data set, try to focus on 
   isolating edge cases
 - Write a PRD view to serve the dashboard
 - Extend the 'iac' lib to update any database object when a change is made to that file. 


### Notes
If the iac lib is to update only changed objects, we should publish this as a git repo and set a precommit hook to trigger the iac lib. Database objects should be stored in an 'obj' directory, and each object should have it's own file so as to isolate each component. 
Re. orchestration, best way is probably to have a procedure for each task, and a master procedure which we trigger programatically using `snowflake-connector-python` based on our watchdog trigger. 

