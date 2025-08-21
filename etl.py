import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries

"""
This script connects to a Redshift/PostgreSQL cluster using parameters from 
the configuration file (dwh.cfg), loads raw data into staging tables from S3 
using COPY commands, and then inserts processed data into analytics tables.

It is part of a data warehouse ETL pipeline where data is staged first and then
transformed into fact and dimension tables.
"""


def load_staging_tables(cur, conn):
    """
    Loads raw data from S3 into staging tables.

    Executes all SQL COPY commands defined in `copy_table_queries`.

    Parameters
    ----------
    cur : psycopg2.extensions.cursor
        Database cursor used to execute SQL queries.
    conn : psycopg2.extensions.connection
        Active database connection to commit transactions.
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
    Inserts data from staging tables into analytics (fact and dimension) tables.

    Executes all SQL INSERT commands defined in `insert_table_queries`.

    Parameters
    ----------
    cur : psycopg2.extensions.cursor
        Database cursor used to execute SQL queries.
    conn : psycopg2.extensions.connection
        Active database connection to commit transactions.
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    - Reads database connection configuration from dwh.cfg.
    - Connects to the Redshift/PostgreSQL cluster.
    - Loads data into staging tables from S3.
    - Inserts processed data into analytics tables.
    - Closes the database connection.
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect(
        "host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values())
    )
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
