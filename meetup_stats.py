"""
meetup_stats allows to download data about meetup.com events into csv files or a postgres database
"""

import csv_writer as csv
import database as db
import meetup_data_collector as meetup


def download_events_to_csv(meetup_group, output_folder):
    """
    Downloads events and attendance data using meetup_data_collector,
    and writes them into csv files using csv_writer.

    param meetup_group: identifier of the meetup group to get data for
    param output_folder: folder to write csv files to
    """
    print(
        f"downloading data for meetup group '{meetup_group}' into folder '{output_folder}'..."
    )

    events = meetup.collect_event_info(meetup_group)

    csv.write_events_overview(events, output_folder)

    for event in events:
        attendees_csv = meetup.collect_event_attendees(event)
        csv.write_attendee_csv(event, attendees_csv, output_folder)


def download_events_to_db(
    meetup_group, host="localhost", port="5432", user="postgres", password="pw"
):
    """
    Downloads events and attendance data using meetup_data_collector,
    and writes them into a postgres database using database

    param meetup_group: identifier of the meetup group to get data for
    param host: host to connect to
    param port: port to connect to
    param user: postgres user to connect as
    param pw: of the postgres user
    """

    print(
        f"downloading data for meetup group '{meetup_group}' to database '{host}:{port}'..."
    )

    conn = db.open_connection(meetup_group, host, port, user, password)

    db.create_tables_if_none_exist(conn)

    events = meetup.collect_event_info(meetup_group)

    for event in events:
        db.add_event_to_db(conn, event)

        attendees_csv = meetup.collect_event_attendees(event)
        db.add_users_to_db(conn, attendees_csv[1:])
        db.add_event_attendance(conn, event["id"], attendees_csv[1:])

    conn.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "meetup",
        help=(
            "The meetup to query for."
            "This needs to be the identifier found in the meetup group's url path."
        ),
    )
    parser.add_argument(
        "command",
        help=(
            "The command to run."
            "Either 'csv' or 'db' downloading data either to csv files or a postgres database."
        ),
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
        download_events_to_csv(args.meetup, args.csv_outputfolder)
    elif args.command == "db":
        download_events_to_db(
            args.meetup, args.db_host, args.db_port, args.db_user, args.db_pw
        )
    else:
        print("unknown command '{}' - needs to be 'csv' or 'db'".format(args.command))
