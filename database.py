"""database offers methods to write event and attendance data to postgres"""

import psycopg2


def open_connection(
    dbname, host="localhost", port="5432", user="postgres", password="pw"
):
    """
    Opens a connection to the given database
    param dbname: name of the db to connect to
    param host: host to connect to
    param port: port to connect to
    param user: postgres user to connect as
    param pw: of the postgres user
    returns: a psycopg2 database connection to use in other methods
    """

    return psycopg2.connect(
        dbname=dbname, host=host, port=port, user=user, password=password
    )


def create_tables_if_none_exist(connection):
    """
    Creates required tables if they don't exist yet
    param connection: a psycopg2 database connection
    """

    cur = connection.cursor()
    try:
        cur.execute(
            """CREATE TABLE events (
                id integer PRIMARY KEY,
                name varchar,
                url varchar,
                date date,
                is_remote bool,
                attendance integer,
                rsvps integer,
                waitlist integer
            );"""
        )
        connection.commit()
    except psycopg2.errors.DuplicateTable:
        print("events table already exists")
        connection.rollback()
    try:
        cur.execute(
            """CREATE TABLE event_attendance (
                event_id integer,
                user_id varchar,
                user_title varchar,
                is_host bool,
                attended bool,
                rsvp_on date,
                PRIMARY KEY(event_id, user_id)
            );"""
        )
        connection.commit()
    except psycopg2.errors.DuplicateTable:
        print("event_attendance table already exists")
        connection.rollback()
    try:
        cur.execute(
            """CREATE TABLE group_members (
                id varchar PRIMARY KEY,
                user_name varchar,
                joined_on date,
                profile_url varchar
            );"""
        )
        connection.commit()
    except psycopg2.errors.DuplicateTable:
        print("group_members table already exists")
        connection.rollback()
    cur.close()


def add_event_to_db(connection, event):
    """
    Writes given event data to database
    param connection: a psycopg2 database connection
    param param event: event tuple to write to DB
    """

    cur = connection.cursor()
    try:
        cur.execute(
            """INSERT INTO events (
                id,
                name,
                url,
                date,
                is_remote,
                attendance,
                rsvps,
                waitlist
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""",
            (
                event["id"],
                event["name"],
                event["url"],
                event["date"],
                event["isRemote"],
                event["attendance"],
                event["rsvps"],
                event["waitlist"],
            ),
        )
        connection.commit()
    except psycopg2.errors.UniqueViolation:
        print("Event '{}' ({}) already exists in DB".format(event["name"], event["id"]))
        connection.rollback()
    cur.close()


def add_users_to_db(connection, event_attendees):
    """
    Write group members to database based on event attendance
    param connection: a psycopg2 database connection
    param event_attendees:  list of attendee information to write to DB
    """

    cur = connection.cursor()
    for attendance in event_attendees:
        name = attendance[1]
        user_id = attendance[2]
        joined = attendance[8]
        profile_url = attendance[9]
        try:
            cur.execute(
                """INSERT INTO group_members (
                    id,
                    user_name,
                    joined_on,
                    profile_url
                ) VALUES(%s, %s, %s, %s);""",
                (user_id, name, joined, profile_url),
            )
            connection.commit()
        except psycopg2.errors.UniqueViolation:
            print("User '{}' ({}) already exists in DB".format(name, user_id))
            connection.rollback()
    cur.close()


def add_event_attendance(connection, event_id, event_attendees):
    """
    Write event attendance records to database
    param connection: a psycopg2 database connection
    param event_id:  id of the event to persist
    param event_attendees:  list of attendee information to write to DB
    """

    cur = connection.cursor()
    for attendance in event_attendees:
        user_id = attendance[2]
        user_title = attendance[3]
        is_host = bool(attendance[4] == "Yes")
        attended = bool(attendance[5] == "Yes")
        rsvp_on = attendance[7]
        try:
            cur.execute(
                """INSERT INTO event_attendance (
                    event_id,
                    user_id,
                    user_title,
                    is_host,
                    attended,
                    rsvp_on
                ) VALUES (%s, %s, %s, %s, %s, %s);""",
                (event_id, user_id, user_title, is_host, attended, rsvp_on),
            )
            connection.commit()
        except psycopg2.errors.UniqueViolation:
            print(
                "Attendance record for event '{}' & user {} already exists in DB".format(
                    event_id, user_id
                )
            )
            connection.rollback()
    cur.close()
