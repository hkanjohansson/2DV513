from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, insert
import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import os

cnx = mysql.connector.connect(user='root',
                              password='root',
                              )

DB_NAME = 'reddit_data'
cursor = cnx.cursor()

def create_database(cursor, DB_NAME):
    try:
        cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8mb4'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

path = os.getcwd() + r'\2DV513_Reddit_Files\RC_2011-07'
engine = create_engine('mysql://root:root@localhost:3306/reddit_data')

columns = ['id', 'parent_id', 'link_id', 'name', 'author', 'body', 'subreddit_id', 'subreddit', 'score', 'created_utc']
reddit_frame = pd.DataFrame(columns=columns)

with pd.read_json(path, lines=True, chunksize=10000) as reader:
    for chunk in reader:
        reddit_frame = pd.concat([reddit_frame, chunk[columns]])
        
try:
    cursor.execute("USE {}".format(DB_NAME)) #"USE reddit_data"
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor, DB_NAME)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
        create_table_comments(cursor)
        insert_into_reddit_data(cursor)
    else:
        print(err)
    
def create_table_comments(cursor):
    create_comments = "CREATE TABLE `reddit_data` (" \
                 "  `id` varchar(8)," \
                 "  `parent_id` varchar(14)," \
                 "  `link_id` varchar(14)," \
                 "  `name` varchar(14)," \
                 "  `author` varchar(50)," \
                 "  `body` TEXT," \
                 "  `subreddit_id` varchar(14)," \
                 "  `subreddit` varchar(50)," \
                 "  `score` int(10)," \
                 "  `created_utc` int(11) " \
                 ") ENGINE=InnoDB"

    try:
        print("Creating table comments: ")
        cursor.execute(create_comments)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")


def create_table_comments_constraints(cursor):
    create_comments = "CREATE TABLE `reddit_data` (" \
                 "  `id` varchar(8) NOT NULL," \
                 "  `parent_id` varchar(14) NOT NULL," \
                 "  `link_id` varchar(14) NOT NULL," \
                 "  `name` varchar(14) NOT NULL," \
                 "  `author` varchar(50) NOT NULL," \
                 "  `body` TEXT NOT NULL," \
                 "  `subreddit_id` varchar(14) NOT NULL," \
                 "  `subreddit` varchar(50) NOT NULL," \
                 "  `score` int(10) NOT NULL," \
                 "  `created_utc` int(11) NOT NULL, " \
                 "  PRIMARY KEY (`id`)" \
                 ") ENGINE=InnoDB"

    try:
        print("Creating table comments: ")
        cursor.execute(create_comments)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")


create_table_comments_constraints(cursor)
data_to_sql = reddit_frame.to_sql('reddit_data', con=engine, if_exists='replace', chunksize=10000, method='multi')
