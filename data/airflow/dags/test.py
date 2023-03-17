from core.requests import RequestApi
from dotenv import load_dotenv

import json
import os

load_dotenv()

api_key = os.getenv("TICKETMASTER_CONSUMER_KEY")



request = RequestApi()

# api_key = "GCk7HQEKA2GygU3r6KcJOxaC6c6nLGGG"
items_by_page = 200
url = f"https://app.ticketmaster.com/discovery/v2/events.json?apikey={api_key}&size={items_by_page}"

response = request.get_endpoint(url)

dict_response = response.json()

embedded = dict_response["_embedded"]

events = embedded["events"]


current_page = int(dict_response["page"]["number"])
total_page = int(dict_response["page"]["totalPages"])

total_items = items_by_page * total_page

temp_path = "/opt/airflow/logs/"
temp_file = f"temp_events_{current_page}_to_{total_page}.json"


for event in events:
    local_file = f"{temp_path}/{temp_file}"

    with open(f"{local_file}", "a") as json_file:
        json.dump(event, json_file)
    json_file.close()
    file = open(local_file, "a")
    file.write("\n")
    file.close()

# print(type(dict_response["_embedded"]))
# print(len(dict_response["_embedded"]))

# print(response.text)
