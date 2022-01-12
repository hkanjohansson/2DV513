from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, insert
import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import os
import numpy as np

np.random.seed(1)

cnx = mysql.connector.connect(user='root',
                              password='root',
                              )

DB_NAME = 'game_reviews'
cursor = cnx.cursor()
engine = create_engine('mysql://root:root@localhost:3306/game_reviews')

games_columns = ['title', 'genre', 'company']
reviewers_columns = ['email', 'country']
reviews_columns = ['title', 'date', 'reviewer', 'review']
#likes_columns = ['up', 'down']

games = np.array([['Super Mario Bros.', 'Platform', 'Nintendo'], ['Metal Gear Solid', 'Action', 'Konami'], ['Pokémon', 'RPG', 'Game Freak Inc.'], 
                ['The Witcher 3', 'RPG', 'CD Project Red'], ['Halo Combat Evolved', 'FPS', 'Bungie'], ['Resident Evil 4', 'Horror', 'Capcom'],
                ['Super Mario Bros. 2', 'Platform', 'Nintendo'], ['Super Mario Bros. 3', 'Platform', 'Nintendo'], ['Divinity Original Sin 2', 'RPG', 'Larian Studios'],
                ['Starcraft 2', 'RTS', 'Blizzard']
                ]).reshape(-1, 3)

reviewers = np.array(
    [['game123@email.com', 'Sweden'], ['game321@email.com', 'Sweden'], ['game12ger@email.com', 'Germany'], 
    ['game55@email.com', 'England'], ['game123@email.com', 'Norway'], ['gamepl@email.com', 'Poland'], ['game1234ger@email.com', 'Germany'], 
    ['game12sk@email.com', 'South Korea'], ['dan_game@email.com', 'Denmark']]
).reshape(-1, 2)

def generate_reviews(columns, n_reviews):
    temp_reviews = []
    
    for i in range(n_reviews):
        temp_reviews.append([games[np.random.randint(0, len(games))][0], np.random.randint(10, 200), reviewers[np.random.randint(0, len(reviewers))][0], 'This is a review'])

    return pd.DataFrame(np.array(temp_reviews).reshape(-1, len(columns)), columns=columns)


reviews = generate_reviews(reviews_columns, 500)
games = pd.DataFrame(games, columns=games_columns)
reviewers = pd.DataFrame(reviewers, columns=reviewers_columns)

def create_database(cursor, DB_NAME):
    try:
        cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8mb4'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


#create_database(cursor, DB_NAME)
games.to_sql('games', con=engine, if_exists='replace')
reviewers.to_sql('reviewer', con=engine, if_exists='replace')
reviews.to_sql('reviews', con=engine, if_exists='replace')