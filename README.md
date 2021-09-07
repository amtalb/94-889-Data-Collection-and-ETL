# 94-889 Data Collection and ETL Assignment
### Alexander Talbott

This repo serves as a home for the first assignment in 94-889 Machine Learning and Public Policy. In this project, I read in data from the US Census API, transformed it, and loaded it into a PostgreSQL database.
(
To read the data from the census website, I utilized the [`censusdata`](https://pypi.org/project/CensusData/) API available on PyPI. Using this API, I only had to specify the "state number" (which is configurable in the config file) and I could get all census blocks groups in that state. 

Then, using a provided list of variables (also configurable), I queried for certain statistics for each of those block groups and stored them in a pandas dataframe. Then, the pandas dataframe is saved as a CSV file to disk.

Using the saved CSV file and the `csvkit` command line tool, I launch a subprocess to run a shell script that uses the `csvsql` utility to generate an SQL `CREATE TABLE` statement in accordance with the columns in the CSV file. Aftering capturing the output of that shell script, I then open up a PostgreSQL database connection and execute the output to create a new database table. 

Finally, the rest of the CSV file (the data) is written to the database using the `copy_from` method from the [`psycopg2`](https://pypi.org/project/psycopg2/) package.