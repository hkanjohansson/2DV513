import mysql.connector
from sqlalchemy import create_engine
from mysql.connector import errorcode
import pandas as pd


cnx = mysql.connector.connect(user='root',
                              password='root',
                              )

DB_NAME = 'game_reviews'
cursor = cnx.cursor()
engine = create_engine('mysql://root:root@localhost:3306/game_reviews')

try:
    cursor.execute("USE {}".format(DB_NAME)) #"USE game_reviews"
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor, DB_NAME)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)

#cursor.execute("DROP VIEW reviews_by_country")
#cursor.execute("DROP VIEW company_reviewed;")

most_reviews = "SELECT title, COUNT(title) as most_reviewed FROM reviews GROUP BY title ORDER BY most_reviewed DESC;"

most_reviews_country_view = "CREATE VIEW reviews_by_country AS SELECT COUNT(COUNTRY) AS n_reviews, country FROM reviewer JOIN reviews ON reviews.reviewer = reviewer.email GROUP BY country ORDER BY n_reviews DESC;"
most_reviews_country = "SELECT * FROM reviews_by_country;"

company_reviewed_view = "CREATE VIEW company_reviewed AS SELECT games.title, games.company, reviews.date, reviews.reviewer, reviews.review FROM reviews JOIN games ON games.title = reviews.title;"
company_reviewed = "SELECT reviewer, title, company, review FROM company_reviewed WHERE reviewer = 'game55@email.com' GROUP BY title;"

popular_genres_view = "CREATE VIEW genres AS SELECT games.title, games.genre FROM games JOIN reviews ON reviews.title = games.title;"
popular_genres = "SELECT COUNT(genre) AS n_genres, genre FROM genres GROUP BY genre ORDER BY n_genres DESC;"

company_most_reviewed_view = "CREATE VIEW company_most_reviews AS SELECT company, COUNT(company) AS n_reviews FROM company_reviewed GROUP BY company ORDER BY n_reviews DESC;"
company_most_reviewed = "SELECT company, MAX(n_reviews) AS most_reviewed FROM company_most_reviews;"

queries = ['Most reviewed game', 'Most reviews by country', 'Which games including title, company, review date and review for a specific user', 'Genres popularity', 'The most popular company']
query_statements = [most_reviews, most_reviews_country, company_reviewed, popular_genres, company_most_reviewed]

print('Choose 1 for retrieving data or 2 for inserting data: ')

init_choice = input()

while init_choice != '1' and init_choice != '2':
    print("Please enter a valid choice")
    init_choice = input()


if init_choice == '1':
    print(f"\nChoose a number between 1 and 5 for the following data:")
    for i in range(len(queries)):
        print(f'{i + 1}: {queries[i]}')
    query_choice = input()
    choices = ['1', '2', '3', '4', '5']

    while query_choice not in choices:
        print(f'\nPlease enter a number betweeen 1 and 5 for the following data:')
        for i in range(len(queries)):
            print(f'{i + 1}: {queries[i]}')
        query_choice = input()

    cursor.execute(query_statements[int(query_choice) - 1])
    for statement in cursor:
        print("{}".format(statement))

elif init_choice == '2':
    print(f'Enter valid data into the database:\n1. Who are you(email, country)? \n2. What game(title, genre, company) \n3. Review(date, review)')
    
    print('Who are you(email, country)? Press enter after each value is inserted')
    who = pd.DataFrame([[input(), input()]], columns=['email', 'country'])
    who.to_sql('reviewer', con=engine, if_exists='append', index=False)

    print('Do you want to review a game? Choose y for yes or anything else for no')
    rev_yes = input() == 'y'
    if rev_yes:
        print('What game(title, genre, company) are you reviewing? Press enter after each value is inserted')
        game_input = [input(), input(), input()]
        game = pd.DataFrame([game_input], columns=['title', 'genre', 'company'])
        game.to_sql('games', con=engine, if_exists='append', index=False)


        print('What is your review(date, review)? Press enter after each value is inserted')
        review = pd.DataFrame([[game.iloc[0]['title'], input(), who.iloc[0]['email'], input()]], columns=['title', 'date', 'reviewer', 'review'])
        review.to_sql('reviews', con=engine, if_exists='append', index=False)
        exit()
    else:
        print('See you later')
        exit()



        