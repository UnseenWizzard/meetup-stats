# Meetup Statistics Export

This is a simple python script to extract data about meetup.com events into csv files or a postgres database.

I was not happy with the statistics the meetup website provides me as a meetup organizer, so I've created this quick and dirty way of grabbing information about a groups events and attendees. 

I use this in combination [Blazer](https://github.com/ankane/blazer) an open source data exploration/Business Intelligence tool to build charts and dashboards for our meetup group [Agile International Graz](https://www.meetup.com/agile-international-graz/).

# What data is exported?

For past Events if your meetup group: 
* id
* name
* date
* is_remote - Boolean indicator whether this was an online or in-person event
* attendance - Number of people who came to the event
* rsvps - Number of people who RSVPed Yes to the event
* waitlist - Number of people on the waitlist

Attendee data per event: 
* Event Name
* Name
* User ID
* Title
* Event Host 
* RSVP
* Guests
* RSVPed on
* Joined Group on
* URL of Member Profile

# How to use

To run locally you need python3 and installed requirements (pip3 install -r requirements.tx).

```shell
python3 meetup_stats.py -h
usage: meetup_stats.py [-h] [--csv-outputfolder CSV_OUTPUTFOLDER] [--db-host DB_HOST] [--db-port DB_PORT] [--db-user DB_USER] [--db-pw DB_PW] meetup command

positional arguments:
  meetup                The meetup to query for. This needs to be the identifier found in the meetup group's url path.
  command               The command to run, either 'csv' or 'db' downloading data either to csv files or a postgres database.

optional arguments:
  -h, --help            show this help message and exit
  --csv-outputfolder CSV_OUTPUTFOLDER
                        folder to write csv files to. Default: output
  --db-host DB_HOST     database host to connect to. Default: localhost
  --db-port DB_PORT     database port to connect to. Default: 5432
  --db-user DB_USER     database user to connect with. Default: postgres
  --db-pw DB_PW         database password to connect with.
```

> **In addition to the command line arguments the script requires your current meetup cookie in an evironment variable named `MEETUP_STATS_MEETUP_COOKIE`!**
> 
> To get the cookie e.g. use the developer tools network tab and copy it from a GET request made while opening meetup.com while logged in.
> 
> Using the meetup API properly with oauth2 app authorization is planned, but for now this does the trick as an MVP.

## Exporting to CSV

```shell
python3 meetup_stats.py my-sample-meetup csv
```

## Exporting to postgres

**This needs a postgres database matching the name of your meetup!**

For example using [the postgres docker image](https://hub.docker.com/_/postgres) this can be done as: 
```shell
docker run --name meetup-postgres -e POSTGRES_DB=my-sample-meetup -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres
```

Then run the script to write to the DB:
```shell
python3 meetup_stats.py my-sample-meetup db --db-pw mysecretpassword
```

# Querying Data from the Database

Now you should be able to access your data. 
Assuming the same postgres container, get the the first ten events via:

```shell
docker exec -it meetup-postgres psql -U postgres -d my-sample-meetup -c "SELECT * FROM events LIMIT 10;"
```

As a starting point on what to do with the data take a look at these [sample queries](./sample_queries.md).