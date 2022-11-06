import csv
import os


def writeEventsOverview(events, outputFolder="output"):
    """
    Writes events list ot to disk
    param events: list of events
    """
    createOutputFolderIfNotExists(outputFolder)

    with open(f"{outputFolder}/events.csv", "w") as csvFile:
        writer = csv.writer(csvFile)
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


def writeAttendeeCsv(event, attendees_csv, outputFolder="output"):
    """
    Writes event attendees to disk
    param event: event tuple:(id, name, url)
    param attendees_csv: list of attendee information
    """
    createOutputFolderIfNotExists(outputFolder)

    with open(f"{outputFolder}/attendees-{event['id']}.csv", "w") as csvFile:
        csv.writer(csvFile).writerows(attendees_csv)


def createOutputFolderIfNotExists(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"created output folder '{path}'")
