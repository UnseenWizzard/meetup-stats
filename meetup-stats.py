import csv_writer as csv
import database as db
import meetup_data_collector as meetup


def downloadEventAttendeeCsvs(meetup_group, outputFolder):
    print(
        f"downloading data for meetup group '{meetup_group}' into folder '{outputFolder}'..."
    )

    events = meetup.collectEventInfo(meetup_group)

    csv.writeEventsOverview(events, outputFolder)

    for event in events:
        attendees_csv = meetup.collectEventAttendees(event)
        csv.writeAttendeeCsv(event, attendees_csv, outputFolder)


def downloadEventsToDB(
    meetup_group, host="localhost", port="5432", user="postgres", password="pw"
):
    print(
        f"downloading data for meetup group '{meetup_group}' to database '{host}:{port}'..."
    )

    conn = db.openConnection(meetup_group, host, port, user, password)

    db.createTablesIfNoneExist(conn)

    events = meetup.collectEventInfo(meetup_group)

    for event in events:
        db.addEventToDb(conn, event)

        attendees_csv = meetup.collectEventAttendees(event)
        db.addUsersToDb(conn, attendees_csv[1:])
        db.addEventAttendance(conn, event["id"], attendees_csv[1:])

    conn.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "meetup",
        help="The meetup to query for. This needs to be the identifier found in the meetup group's url path.",
    )
    parser.add_argument(
        "command",
        help="The command to run, either 'csv' or 'db' downloading data either to csv files or a postgres database.",
    )

    parser.add_argument(
        "--csv-outputfolder",
        help="folder to write csv files to. Default: output",
        default="output",
    )

    parser.add_argument(
        "--db-host",
        help="database host to connect to. Default: localhost",
        default="localhost",
    )
    parser.add_argument(
        "--db-port", help="database port to connect to. Default: 5432", default="5432"
    )
    parser.add_argument(
        "--db-user",
        help="database user to connect with. Default: postgres",
        default="postgres",
    )
    parser.add_argument("--db-pw", help="database password to connect with.")

    args = parser.parse_args()

    if args.command == "csv":
        downloadEventAttendeeCsvs(args.meetup, args.csv_outputfolder)
    elif args.command == "db":
        downloadEventsToDB(
            args.meetup, args.db_host, args.db_port, args.db_user, args.db_pw
        )
    else:
        print("unknown command '{}' - needs to be 'csv' or 'db'".format(args.command))
