SHOW DATABASES;
#DROP DATABASE game_reviews;
USE game_reviews;

/*
ALTER TABLE games
DROP COLUMN `index`;

ALTER TABLE reviewer
DROP COLUMN `index`;

ALTER TABLE reviews
DROP COLUMN `index`;
*/

/*
CREATE TABLE Games (
	
	title VARCHAR(255) NOT NULL,
    genre VARCHAR(255),
    company VARCHAR(255)
    
);

CREATE TABLE Reviewer (
	id INT NOT NULL AUTO_INCREMENT,
	email VARCHAR(255) NOT NULL,
    country VARCHAR(255),
    PRIMARY KEY (id)
);


CREATE TABLE Reviews (
	id INT NOT NULL AUTO_INCREMENT,
	title VARCHAR(255),
    date VARCHAR(255),
    email VARCHAR(255),
    review TEXT,
    reviewer TEXT,
    PRIMARY KEY (id)
);
*/
SHOW TABLES;

SELECT *
FROM games;	

SELECT COUNT(*)
FROM games AS temp;

SELECT *
FROM reviewer;

SELECT *
FROM reviews
WHERE reviewer='hj222je@student.lnu.se';

# Which title has the most reviews?
SELECT title, COUNT(title) as most_reviewed
FROM reviews
GROUP BY title
ORDER BY most_reviewed DESC;

# Which country has made the most reviews?
DROP VIEW reviews_by_country;
CREATE VIEW reviews_by_country AS
SELECT COUNT(COUNTRY) AS n_reviews, country
FROM reviewer
JOIN reviews ON reviews.reviewer = reviewer.email
GROUP BY country
ORDER BY n_reviews DESC;

SELECT *
FROM reviews_by_country;

# Which games and by what company is those games made by has a specific user reviewed?
DROP VIEW company_reviewed;
CREATE VIEW company_reviewed AS
SELECT games.title, games.company, reviews.date, reviews.reviewer, reviews.review
FROM reviews
JOIN games ON games.title = reviews.title;

SELECT reviewer, title, company, review
FROM company_reviewed
WHERE reviewer = 'game55@email.com'
GROUP BY title;

# What genre is the most popular (n_reviews) in each country represented in the database?
DROP VIEW genres;
CREATE VIEW genres AS
SELECT games.title, games.genre
FROM games
JOIN reviews ON reviews.title = games.title;

SELECT *
FROM genres;

SELECT COUNT(genre) AS n_genres, genre
FROM genres
GROUP BY genre
ORDER BY n_genres DESC;

# Which company has the most reviews?
DROP VIEW company_most_reviews;
CREATE VIEW company_most_reviews AS
SELECT company, COUNT(company) AS n_reviews
FROM company_reviewed
GROUP BY company
ORDER BY n_reviews DESC;

SELECT company, MAX(n_reviews) AS most_reviewed
FROM company_most_reviews;



/*
Write queries to show if there are any users that has not written any reviews. 
(Change table name of Reviewer to User?)
*/

SELECT reviewer, COUNT(reviewer) AS n_reviews
FROM reviews
GROUP BY reviewer
ORDER BY n_reviews DESC;

SELECT email, country 
FROM reviewer
WHERE email 
NOT IN (
	SELECT reviewer
    FROM reviews
);
