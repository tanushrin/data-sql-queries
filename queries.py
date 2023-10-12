# pylint: disable=C0103, missing-docstring

def detailed_movies(db):
    '''return the list of movies with their genres and director name'''
    query = "SELECT m.title, m.genres, d.name \
            from movies m \
            JOIN directors d ON m.director_id = d.id "
    db.execute(query)
    results = db.fetchall()
    return results


def late_released_movies(db):
    '''return the list of all movies released after their director death'''
    query = "SELECT m.title from movies m \
            JOIN directors d ON m.director_id = d.id \
            WHERE  m.start_year > d.death_year \
            ORDER BY m.title"
    db.execute(query)
    results = db.fetchall()
    return [movie[0] for movie in results]


def stats_on(db, genre_name):
    '''return a dict of stats for a given genre'''
    query = f"SELECT COUNT(m.id), AVG(m.minutes) \
            FROM movies m \
            WHERE m.genres = '{genre_name}'"
    db.execute(query)
    results = db.fetchall()
    #print(results)
    dict1={}
    dict1['genre'] = genre_name
    dict1['number_of_movies'] = results[0][0]
    dict1['avg_length'] = round(results[0][1],2)
    return dict1


def top_five_directors_for(db, genre_name):
    '''return the top 5 of the directors with the most movies for a given genre'''
    query = f"SELECT d.name  , COUNT(m.title) as no_of_movies \
            FROM movies m \
            JOIN directors d  ON m.director_id = d.id \
            WHERE m.genres = '{genre_name}'\
            GROUP BY d.name \
            ORDER BY no_of_movies DESC , d.name ASC \
            LIMIT 5"
    db.execute(query)
    results = db.fetchall()
    return results


def movie_duration_buckets(db):
    '''return the movie counts grouped by bucket of 30 min duration'''
    max_duration_query = "SELECT MAX(m.minutes) FROM movies m"
    db.execute(max_duration_query)
    results = db.fetchone()
    max_duration = int(results[0])

    bucket_width = 30
    number_of_buckets = round(max_duration / bucket_width)
    lst = []

    for i in range(number_of_buckets+1):
        #--SELECT COUNT(*) FROM movies WHERE minutes < 30
        #SELECT COUNT(*) FROM movies WHERE minutes < 60 and minutes >= 30

        query = f'SELECT COUNT(*) FROM movies WHERE \
            minutes < {bucket_width*(i+1)} and minutes >= {bucket_width*i}'
        db.execute(query)
        results = db.fetchall()
        if results[0][0] != 0:
            tup = (bucket_width*(i+1), results[0][0])
            lst.append(tup)
        #print(lst)
    return lst


def top_five_youngest_newly_directors(db):
    '''return the top 5 youngest directors when they direct their first movie'''
    query = "SELECT d.name, \
    (m.start_year-d.birth_year) as age_when_first_time_director \
    FROM movies m \
    JOIN directors d   ON m.director_id = d.id \
    WHERE d.birth_year IS NOT NULL \
    ORDER BY age_when_first_time_director ASC LIMIT 5"
    db.execute(query)
    results = db.fetchall()
    return results
