import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries

"""
This script connects to a Redshift/PostgreSQL cluster using parameters from 
the configuration file (dwh.cfg), drops existing tables, and recreates them.

It is part of a data warehouse setup pipeline where staging and analytics tables
are created before loading data.
"""


def drop_tables(cur, conn):
    """
    Drops all tables defined in the `drop_table_queries` list.

    Parameters
    ----------
    cur : psycopg2.extensions.cursor
        Database cursor used to execute SQL queries.
    conn : psycopg2.extensions.connection
        Active database connection to commit transactions.
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Creates all tables defined in the `create_table_queries` list.

    Parameters
    ----------
    cur : psycopg2.extensions.cursor
        Database cursor used to execute SQL queries.
    conn : psycopg2.extensions.connection
        Active database connection to commit transactions.
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    - Reads database connection configuration from dwh.cfg.
    - Connects to the Redshift/PostgreSQL cluster.
    - Drops existing tables.
    - Creates new tables.
    - Closes the database connection.
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect(
        "host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values())
    )
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
