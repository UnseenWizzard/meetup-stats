# Group Member Information

## Group Joins

```sql
SELECT joined_on, count(joined_on)
FROM "group_members"
GROUP BY joined_on;
```

## Top Group Members

```sql
SELECT m.user_name as name, count(event_id) as attended_events
FROM "event_attendance" a
    JOIN "group_members" m on a.user_id = m.id
WHERE NOT a.is_host
GROUP BY name
ORDER BY attended_events DESC;
```

# Event Information

## On Site Attendance

```sql
SELECT date, rsvps, attendance
FROM "events"
WHERE NOT is_remote;
```

## Remote Attendance

```sql
SELECT date, rsvps, attendance
FROM "events"
WHERE is_remote;
```

## Show Rate

```sql
SELECT 
    avg(100.0*attendance/rsvps) as average_show_rate,
    (SELECT avg(100.0*attendance/rsvps) FROM "events" WHERE is_remote) as remote_show_rate,
    (SELECT avg(100.0*attendance/rsvps) FROM "events" WHERE not is_remote) as onsite_show_rate
FROM "events";
```

## Show Rate per Event

```sql
SELECT date, name, rsvps, attendance, ROUND(100.0*attendance/rsvps,2) as show_rate 
FROM "events"
ORDER BY date DESC;
```
