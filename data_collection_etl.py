import subprocess

import censusdata
import pandas as pd
import psycopg2
import yaml


def get_census_data(state_number, year, var):
    # getting blocks
    # TODO
    # add options for geography
    geo = censusdata.censusgeo(
        [("state", str(state_number)), ("county", "*"), ("block group", "*")]
    )
    print("downloading census data")
    df = censusdata.download("acs5", year, geo, var)

    # remove commas
    df = df.replace(",", "")

    return df


def write_to_db(db_info):
    command = """
        CREATE SCHEMA IF NOT EXISTS acs;

        DROP TABLE IF EXISTS acs.atalbott_acs_data;
        """

    create_table_script = subprocess.run(
        [
            "sh",
            "./generate_create_table_statements.sh",
            "output.csv",
            "acs",
            "atalbott_acs_data",
        ],
        capture_output=True,
    ).stdout.decode("utf8")

    command += create_table_script

    try:
        print("connecting to db")
        # connect to db
        conn = psycopg2.connect(
            host=db_info["host"],
            port=db_info["port"],
            database=db_info["database"],
            user=db_info["user"],
            password=db_info["password"],
        )
        cur = conn.cursor()

        # build the table
        cur.execute(command)

        # write csv to db
        with open("./output.csv", "r") as f:
            cur.copy_expert("COPY acs.atalbott_acs_data FROM STDIN WITH CSV HEADER", f)

        cur.close()
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        if conn:
            conn.close()


def main(year, state_number, var, db_info):
    # export blocks and variable info to csv file
    df = get_census_data(state_number, year, var)

    # export to csv
    print("exporting csv")
    censusdata.exportcsv("output.csv", df)

    # write csv to db
    write_to_db(db_info)


if __name__ == "__main__":
    with open("config.yaml", "r") as f:
        config_vars = yaml.safe_load(f)
    year = config_vars["year"]
    state_number = config_vars["state_number"]
    var = config_vars["var"]
    db_info = config_vars["db_info"]

    main(year, state_number, var, db_info)
