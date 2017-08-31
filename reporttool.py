# import psycopg2 to work with database
import psycopg2

# variable to store database name.
DBNAME = "news"


# this is a view created for the most errors function at bottom
def log_error_status():
    try:
        db = psycopg2.connect(database=DBNAME)
        c = db.cursor()
        query = """CREATE or REPLACE view error_log AS
                WITH errorrequests AS(
                SELECT time::date AS date, COUNT(*) AS count
                FROM log WHERE log.status = '404 NOT FOUND'
                GROUP BY time::date
                ),
                allrequests AS (
                SELECT time::date AS date, COUNT(*) AS count
                FROM log 
                GROUP BY time::date
                )
                SELECT errorrequests.date, CAST(
                errorrequests.count AS FLOAT
                ) / allrequests.count FROM errorrequests, allrequests
                WHERE errorrequests.date = allrequests.date
                AND cast(errorrequests.count AS FLOAT) / allrequests.count > 0.01;
        """
        c.execute(query)
        db.commit()
        db.close()
    except:
        print(" there was an error creating view ")


def popular_articles():
    """this prints the most popular articles"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    # this query finds the most popular articles
    c.execute("""
              SELECT articles.title, count(*) as views 
              FROM articles LEFT JOIN log ON log.path LIKE CONCAT('%', articles.slug)
              GROUP BY articles.title ORDER BY views DESC LIMIT 3
              """)
    results = c.fetchall()
    db.close()
    # this code loops through to find most popular articles
    print("\n- The most popular articles: -\n")
    for i in results:
        print("%s -- %s views" % (i[0], i[1]))


def popular_article_authors():
    """Prints the most popular authors"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    # this query finds the most popular authors
    c.execute("""
                SELECT authors.name,  count(log.path) AS count
                FROM authors LEFT JOIN articles ON authors.id = articles.author 
                LEFT JOIN log ON log.path LIKE CONCAT('%', articles.slug)
                GROUP BY authors.name 
                ORDER BY count LIMIT 3
                """)
    results = c.fetchall()
    db.close()
    # this code loops through to find 3 of the most popular authors
    print("\n- List of the most popular Authors: -\n")
    for i in results:
        print("%s -- %s views" % (i[0], i[1]))



def most_errors():
    """Prints out the most request errors for a given day"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    # this is a select query to get results for most errors reported
    c.execute("SELECT * FROM error_log")
    results = c.fetchall()
    db.close()
    # this loops through to find one day that had the most errors
    print("\n- Days where Errors were more then 1% of total views -\n ")
    for i in results:
        print("%s - %s%% errors " % (i[0], round(i[1] * 100, 2)))
        print("\n")


# code to call all the functions from above.
if __name__ == "__main__":
    # this calls the views created from above
    log_error_status()

    # this calls the functions above
    popular_articles()
    popular_article_authors()
    most_errors()
