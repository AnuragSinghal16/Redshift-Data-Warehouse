# Sparkify Song Play Analysis with Redshift

## Project Overview

Sparkify is a startup building a music streaming app. They want to analyze user activity and song play data to better understand customer behavior.
Currently, all their JSON logs of user activity and song metadata reside in AWS S3. Running analytics directly on this raw data is inefficient.

This project builds a cloud-based data warehouse in Amazon Redshift with a star schema optimized for analytical queries on song plays. An ETL pipeline is implemented to load raw data from S3 into staging tables, transform it, and populate the fact and dimension tables.

## Database Schema Design

The schema follows a star schema pattern for efficient querying.

### Fact Table

`songplays` – records in event data associated with song plays
(songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)

### Dimension Tables

`users` – app users
(user_id, first_name, last_name, gender, level)

`songs` – songs in the music database
(song_id, title, artist_id, year, duration)

`artists` – artists in the music database
(artist_id, name, location, latitude, longitude)

`time` – timestamps broken down into units
(start_time, hour, day, week, month, year, weekday)

Staging tables (staging_events, staging_songs) are used to hold raw S3 data before transformation.

## ETL Pipeline

Extract: Load raw JSON data from S3 buckets into staging tables in Redshift.

Event logs: s3://udacity-dend/log_data

Song metadata: s3://udacity-dend/song_data

Transform: Filter, clean, and join staging data.

Load: Insert data into fact and dimension tables following the star schema.

## Project Files

create_tables.py – drops and creates fact/dimension tables. Run this before ETL.

etl.py – extracts data from S3, loads into staging tables, transforms and inserts into analytics tables.

sql_queries.py – contains SQL queries for table creation, dropping, and insertion.

dwh.cfg – configuration file with Redshift cluster and S3 info. (not uploaded)
