import psycopg2


def openConnection(
    dbname, host="localhost", port="5432", user="postgres", password="pw"
):
    return psycopg2.connect(
        dbname=dbname, host=host, port=port, user=user, password=password
    )


def createTablesIfNoneExist(connection):
    cur = connection.cursor()
    try:
        cur.execute(
            "CREATE TABLE events (id integer PRIMARY KEY, name varchar, url varchar, date date, is_remote bool, attendance integer, rsvps integer, waitlist integer);"
        )
        connection.commit()
    except psycopg2.errors.DuplicateTable:
        print("events table already exists")
        connection.rollback()
        pass
    try:
        cur.execute(
            "CREATE TABLE event_attendance (event_id integer, user_id varchar, user_title varchar, is_host bool, attended bool, rsvp_on date, PRIMARY KEY(event_id, user_id));"
        )
        connection.commit()
    except psycopg2.errors.DuplicateTable:
        print("event_attendance table already exists")
        connection.rollback()
        pass
    try:
        cur.execute(
            "CREATE TABLE group_members (id varchar PRIMARY KEY, user_name varchar, joined_on date, profile_url varchar);"
        )
        connection.commit()
    except psycopg2.errors.DuplicateTable:
        print("group_members table already exists")
        connection.rollback()
        pass
    cur.close()


def addEventToDb(connection, event):
    cur = connection.cursor()
    try:
        cur.execute(
            "INSERT INTO events (id, name, url, date, is_remote, attendance, rsvps, waitlist) VALUES(%s, %s, %s, %s, %s, %s, %s, %s);",
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


def addUsersToDb(connection, eventAttendees):
    cur = connection.cursor()
    for attendance in eventAttendees:
        name = attendance[1]
        id = attendance[2]
        joined = attendance[8]
        profile_url = attendance[9]
        try:
            cur.execute(
                "INSERT INTO group_members (id, user_name, joined_on, profile_url) VALUES(%s, %s, %s, %s);",
                (id, name, joined, profile_url),
            )
            connection.commit()
        except psycopg2.errors.UniqueViolation:
            print("User '{}' ({}) already exists in DB".format(name, id))
            connection.rollback()
    cur.close()


def addEventAttendance(connection, eventId, eventAttendees):
    cur = connection.cursor()
    for attendance in eventAttendees:
        user_id = attendance[2]
        user_title = attendance[3]
        is_host = True if attendance[4] == "Yes" else False
        attended = True if attendance[5] == "Yes" else False
        rsvp_on = attendance[7]
        try:
            cur.execute(
                "INSERT INTO event_attendance (event_id, user_id, user_title, is_host, attended, rsvp_on) VALUES(%s, %s, %s, %s, %s, %s);",
                (eventId, user_id, user_title, is_host, attended, rsvp_on),
            )
            connection.commit()
        except psycopg2.errors.UniqueViolation:
            print(
                "Attendance record for event '{}' & user {} already exists in DB".format(
                    eventId, user_id
                )
            )
            connection.rollback()
    cur.close()
