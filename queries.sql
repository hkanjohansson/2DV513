#DROP DATABASE reddit_data;
SHOW DATABASES;
USE reddit_data;
SHOW TABLES;

SELECT *
FROM reddit_data;

SELECT COUNT(*)
FROM reddit_data;
# 1
SELECT author, COUNT(author) AS occurrences
FROM reddit_data
WHERE author = 'gigaquack';

# 2 (is to cumbersome for now... might be easier if the unix timestamp could be converted?)

# 3
SELECT COUNT(body) AS "N comments Contains 'lol'"
FROM reddit_data
WHERE body LIKE '%lol%';

# 4 
SELECT author, link_id, subreddit_id, subreddit
FROM reddit_data
WHERE link_id = 't3_2zufu'
GROUP BY author;

# 5
SELECT author, SUM(score) AS total_score
FROM reddit_data
GROUP BY author
ORDER BY total_score DESC;

# 6 Two queries to answer the question in the assignment
SELECT subreddit, MAX(total_score)
FROM (SELECT subreddit, SUM(score) AS total_score 
FROM reddit_data
GROUP BY subreddit
ORDER BY total_score DESC
) AS t;

SELECT subreddit, MIN(total_score)
FROM (SELECT subreddit, SUM(score) AS total_score 
FROM reddit_data
GROUP BY subreddit
ORDER BY total_score ASC
) AS t;

# 7
SELECT DISTINCT(link_id) AS distinct_link, author 
FROM (
SELECT author, link_id
FROM reddit_data
WHERE author = 'gigaquack'
) AS interacted_with
JOIN distinct_link ON reddit_data.link_id = distinct_link;

# 8
SELECT DISTINCT(author), subreddit
FROM reddit_data
GROUP BY author;

#DROP TABLE reddit_data;