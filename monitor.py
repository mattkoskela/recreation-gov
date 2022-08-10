#!/usr/bin/env python3
import os
import time
import requests
from dotenv import load_dotenv

import helpers

load_dotenv(".env")

SLACK_WEBHOOK = os.environ.get("SLACK_WEBHOOK")


date = input("Reservation date (YYYY-MM-DD): ")
try:
    helpers.validators.validate_date(date)
except ValueError as error:
    print(error)
    exit()

link = input("Recreation.gov Reservation URL (https://www.recreation.gov/ticket/253731/ticket/255): ")
try:
    helpers.validators.validate_recreation_link(link)
except ValueError as error:
    print(error)
    exit()

print(f"date: {date}")
print(f"link: {link}")

facility_id = link.split("/")[4]
tour_id = link.split("/")[6]
year = date.split("-")[0]
month = date.split("-")[1]

i = 0
while True:
    print("checking")

    url = f"https://www.recreation.gov/api/ticket/availability/facility/{facility_id}/monthlyAvailabilitySummaryView?year={year}&month={month}&inventoryBucket=FIT&tourId={tour_id}"
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Request rejected")

    results = response.json().get("facility_availability_summary_view_by_local_date").get(date)
    availability_level = results["availability_level"]
    reservable = results.get("tour_availability_summary_view_by_tour_id").get(tour_id).get("reservable")

    if availability_level != "NONE" or reservable > 0:
        print("Ticket available!")
        helpers.slack.send_message("Recreation.gov ticket available", webhook_url=SLACK_WEBHOOK)
        break

    time.sleep(60)
