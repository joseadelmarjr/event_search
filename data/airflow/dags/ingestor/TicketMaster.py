import json
import os


class TicketMasterApi:
    def __init__(self, start_datetime, end_datetime):
        from dotenv import load_dotenv

        load_dotenv()

        self.current_page = 0
        self.items_by_page = 200
        self.api_limit_items = 1000
        self.api_key = os.getenv("TICKETMASTER_CONSUMER_KEY")
        self.temp_path = os.getenv("DEFAULT_TEMP_PATH")

        self.started = False

        self.start_datetime = start_datetime.strftime('%Y-%m-%dT%H:%M:%SZ')
        self.end_datetime = end_datetime.strftime('%Y-%m-%dT%H:%M:%SZ')


    def __mount_url(self):
        self.url = f"https://app.ticketmaster.com/discovery/v2/events.json?apikey={self.api_key}&size={self.items_by_page}&page={self.current_page}"
        self.url = f"{self.url}&startDateTime={self.start_datetime}&endDateTime={self.end_datetime}"

    
    def get_events(self):
        from core.requests import RequestApi

        request = RequestApi()

        self.__mount_url()
        self.started = True

        print(self.url)
        response = request.get_endpoint(self.url)

        dict_response = response.json()
        embedded = dict_response["_embedded"]

        self.current_page = int(dict_response["page"]["number"])
        self.total_page = int(dict_response["page"]["totalPages"])

        self.events = embedded["events"]


    def save_events(self):
        # temp_path = "/opt/airflow/logs/"
        temp_file = f"tmp_{self.start_datetime}_{self.end_datetime}_page_{self.current_page}_to_{self.total_page - 1}.json"

        for event in self.events:
            local_file = f"{self.temp_path}/{temp_file}"

            with open(f"{local_file}", "a") as json_file:
                json.dump(event, json_file)
            json_file.close()
            file = open(local_file, "a")
            file.write("\n")
            file.close()


    def is_finished(self):

        if not self.started:
            return False

        total_items = self.items_by_page * self.total_page

        if total_items > self.api_limit_items:
            limit_page = self.api_limit_items / self.items_by_page
        else:
            limit_page = self.total_page

        if self.current_page < limit_page:
            return False
        else:
            return True


    def next_page(self):
        self.current_page += 1