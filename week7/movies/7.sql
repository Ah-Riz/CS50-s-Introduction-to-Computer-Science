SELECT title, rating FROM movies, ratings
WHERE movies.id = ratings.movie_id
AND year = 2010
AND rating NOT NULL
ORDER BY rating DESC, title ASC;