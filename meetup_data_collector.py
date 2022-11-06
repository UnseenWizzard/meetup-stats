from urllib.request import Request
import urllib.request
import os
import json


base_url = "https://www.meetup.com"
meetup_cookie = os.getenv("MEETUP_STATS_MEETUP_COOKIE")


def collectEventInfo(meetup_group):
    """
    Collects meetup event id, name and url by scraping past event site.
    returns: list of events tuple:(id, name, url)
    """

    api_query = (
        f"{base_url}/mu_api/urlname/events/past?queries=(endpoint:{meetup_group}/events,"
        f"list:(dynamicRef:list_events_{meetup_group}_past_cancelled,merge:()),meta:(method:get),"
        "params:(desc:true,fields:%27attendance_count,comment_count,event_hosts,featured_photo,plain_text_no_images_description,series,self,rsvp_rules,rsvp_sample,venue,venue_visibility,pro_network_event%27,has_ended:true,status:%27upcoming,past,cancelled%27),"
        f"ref:events_{meetup_group}_past_cancelled)"
    )

    response = makeHttpCall(api_query)

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


def collectEventAttendees(event):
    """
    Collects event attendees for given even
    param event: event tuple:(id, name, url)
    returns: list of events attendee details, first element is csv header row
    """
    attendees_txt = makeHttpCall(event["url"] + "csv")

    attendees_list = attendees_txt.split("\n")
    attendees_csv = []
    for a in attendees_list:
        attendee_info_list = [event["name"]]
        attendee_info_list.extend(a.split("\t"))

        if len(attendee_info_list) == 10:  # filter invalid returns
            attendees_csv.append(attendee_info_list)
    attendees_csv[0][0] = "Event Name"  # loop also writes the actual event name to header element
    return attendees_csv


def makeHttpCall(path):
    req = Request(path)
    req.add_header("Cookie", meetup_cookie)
    contents = urllib.request.urlopen(req).read().decode("utf-8")
    return contents
