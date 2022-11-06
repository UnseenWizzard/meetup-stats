"""csv_writer offers methods to write event and attendance data to csv files"""

import csv
import os


def write_events_overview(events, output_folder="output"):
    """
    Writes events list ot to disk
    param events: list of events
    """
    create_output_folder(output_folder)

    with open(f"{output_folder}/events.csv", "w") as csv_file:
        writer = csv.writer(csv_file)
        header = ["id", "name", "date", "is_remote", "attendance", "rsvps", "waitlist"]
        writer.writerow(header)

        for event in events:
            writer.writerow(
                [
                    event["id"],
                    event["name"],
                    event["url"],
                    event["date"],
                    event["isRemote"],
                    event["attendance"],
                    event["rsvps"],
                    event["waitlist"],
                ]
            )


def write_attendee_csv(event, attendees_csv, output_folder="output"):
    """
    Writes event attendees to disk
    param event: event tuple
    param attendees_csv: list of attendee information
    """
    create_output_folder(output_folder)

    with open(f"{output_folder}/attendees-{event['id']}.csv", "w") as csv_file:
        csv.writer(csv_file).writerows(attendees_csv)


def create_output_folder(path):
    """
    Creates a folder at the given path if it does not already exist
    param path: path of folder to create
    """
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"created output folder '{path}'")
