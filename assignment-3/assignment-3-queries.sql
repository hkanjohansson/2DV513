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

SELECT *
FROM reviewer;

SELECT *
FROM reviews;

# Which titles has the largest amount of reviews?
SELECT title, COUNT(title) as most_reviewed
FROM reviews
GROUP BY title
ORDER BY most_reviewed DESC;

# Which countries has made the most reviews?
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
SELECT games.title, games.company, reviews.reviewer
FROM reviews
JOIN games ON games.title = reviews.title;

SELECT *
FROM company_reviewed;

SELECT title, company
FROM company_reviewed
WHERE reviewer = 'game55@email.com'
GROUP BY title;

# What genres are the most popular (n_reviews)?
DROP VIEW genres;
CREATE VIEW genres AS
SELECT games.title, games.genre, games.company, reviews.reviewer
FROM games
JOIN reviews ON reviews.title = games.title;

SELECT genre, COUNT(genre) AS n_genres
FROM genres
GROUP BY genre
ORDER BY n_genres DESC;

SELECT title, company
FROM genres
WHERE reviewer = 'game55@email.com'
GROUP BY title;

# Which company has the most reviews?
DROP VIEW company_most_reviews;
CREATE VIEW company_most_reviews AS
SELECT company, COUNT(company) AS n_reviews
FROM company_reviewed
GROUP BY company
ORDER BY n_reviews DESC;

SELECT company, MAX(n_reviews) AS most_reviewed
FROM company_most_reviews;

# Which reviewers has not yet made a single review?
SELECT email AS no_reviews
FROM reviewer
WHERE email 
NOT IN (
	SELECT reviewer
    FROM reviews
);
