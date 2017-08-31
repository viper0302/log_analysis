# Udacity Log Analysis Project

A reporting tool that uses information gathered from a database on a 
webserver to answer 3 questions. (Project [Full Stack Web Developer](https://classroom.udacity.com/nanodegrees/nd004/parts/8d3e23e1-9ab6-47eb-b4f3-d5dc7ef27bf0/modules/bc51d967-cb21-46f4-90ea-caf73439dc59/lessons/262a84d7-86dc-487d-98f9-648aa7ca5a0f/concepts/079be127-2d22-4c62-91a8-aa031e760eb0)
* What are the most popular articles?
* Who are the most popular authors?
* What days did more then 1% of requests lead to errors?

## Getting Started
* You will need to install [vagrant](https://www.vagrantup.com/downloads.html)and a[virtual machine](https://www.virtualbox.org/wiki/Downloads)
* Then download the FSND file from[Udacity Full Stack Web Developer](https://classroom.udacity.com/nanodegrees/nd004/parts/8d3e23e1-9ab6-47eb-b4f3-d5dc7ef27bf0/modules/bc51d967-cb21-46f4-90ea-caf73439dc59/lessons/5475ecd6-cfdb-4418-85a2-f2583074c08d/concepts/14c72fe3-e3fe-4959-9c4b-467cf5b7c3a0)
* Then you must have Postgresql newsdata.sql running from the FSND virtual machine
* From the vagrant directory run ```vagrant up```.
* Then SSH into the virtual machine with ```vagrant ssh```.
* Then connect to the news database with ```psql -d news```.
* Then we will need to create a database view if python view is commented out.
```
    CREATE or REPLACE view error_log AS
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

```
* If view is created you should be able to run the reporting tool with:
```
python reporttool.py

```
* If all is good you should get an output with the answers to the 3 questions.




### Languages used

* Postgresql/Database 
* pyscopg2
* Python



