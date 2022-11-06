"""meetup_data_collector offers methods to query event and attendance info from meetup.com"""

from urllib.request import Request
import urllib.request
import os
import json


BASE_URL = "https://www.meetup.com"
MEETUP_COOKIE = os.getenv("MEETUP_STATS_MEETUP_COOKIE")


def collect_event_info(meetup_group):
    """
    Collects meetup event id, name and url by scraping past event site.
    returns: list of events dict(id, url, name, date, is_remote, attendance, rsvps, waitlist)
    """

    api_query = (
        f"{BASE_URL}/mu_api/urlname/events/past?queries=(endpoint:{meetup_group}/events,"
        f"list:(dynamicRef:list_events_{meetup_group}_past_cancelled,merge:()),meta:(method:get),"
        "params:(desc:true,fields:%27attendance_count,comment_count,event_hosts,featured_photo,"
        "plain_text_no_images_description,series,self,rsvp_rules,rsvp_sample,venue,"
        "venue_visibility,pro_network_event%27,has_ended:true,status:%27upcoming,past,"
        "cancelled%27),"
        f"ref:events_{meetup_group}_past_cancelled)"
    )

    response = http_get(api_query)

    response_json = json.loads(response)

    past_events = response_json["responses"][0]["value"]

    events = []

    for event in past_events:
        events.append(
            {
                "id": event["id"],
                "url": event["link"],
                "name": event["name"],
                "date": event["local_date"],
                "isRemote": event["is_online_event"],
                "attendance": event["attendance_count"],
                "rsvps": event["yes_rsvp_count"],
                "waitlist": event["waitlist_count"],
            }
        )

    return events


def collect_event_attendees(event):
    """
    Collects event attendees for given even
    param event: event tuple - as returned by collect_event_info
    returns: list of events attendee details, first element is csv header row
    """
    attendees_txt = http_get(event["url"] + "csv")

    attendees_list = attendees_txt.split("\n")
    attendees_csv = []
    for attendee in attendees_list:
        attendee_info_list = [event["name"]]
        attendee_info_list.extend(attendee.split("\t"))

        if len(attendee_info_list) == 10:  # filter invalid returns
            attendees_csv.append(attendee_info_list)
    attendees_csv[0][0] = "Event Name"  # correctly set added Name header row
    return attendees_csv


def http_get(path):
    """http get request to given path sending MEETUP_COOKIE as header"""
    req = Request(path)
    req.add_header("Cookie", MEETUP_COOKIE)
    contents = ""
    with urllib.request.urlopen(req) as response:
        contents = response.read().decode("utf-8")
    return contents
