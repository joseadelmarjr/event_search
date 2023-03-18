import logging
import pandas as pd
import requests
import os

from bs4 import BeautifulSoup


class SymplaCrawler:
    def __init__(self):
        from dotenv import load_dotenv

        load_dotenv()

        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        self.current_page = 1
        self.limit_page = 10

        self.temp_path = os.getenv("DEFAULT_TEMP_PATH")

        self.started = False


    def __mount_url(self):
        self.url = f"https://www.sympla.com.br/eventos/sao-paulo-sp/todos-eventos?ordem=date&page={self.current_page}"


    def get_events(self):
        from core.requests import RequestApi

        request = RequestApi()

        self.__mount_url()
        self.started = True

        response = request.get_endpoint(self.url)

        soup = BeautifulSoup(response.text, 'html.parser')

        divs = soup.find_all("div")

        div_list = []

        for div in divs:
            div_dict = {}

            try:
                classes_name = div['class']
                div_dict["classes_name"] = classes_name

            except Exception as e:
                div_dict["classes_name"] = ["NA"]

                logging.warning("Nao tem classe")

            try:
                id = div['id']
                div_dict["id"] = id

            except Exception as e:
                div_dict["id"] = "NA"
                logging.warning("Nao tem Id")

            try:
                a_tag = div.find('a')
                a_tag_title = a_tag.get("title")
                a_tag_href = a_tag.get("href")
                div_dict["a_tag_title"] = a_tag_title
                div_dict["a_tag_href"] = a_tag_href

            except Exception as e:
                div_dict["a_tag_title"] = "NA"
                div_dict["a_tag_href"] = "NA"
                logging.warning("Nao tem a_tag")

            div_list.append(div_dict)


        event_list = []
        for my_div in div_list:
            classes_name = my_div["classes_name"]
            event = {}
            criterial = "CustomGridstyle"
            criterial_list = list(filter(lambda item: criterial in item, classes_name))

            if criterial_list:
                event["title"] = my_div["a_tag_title"]
                event["link_detail"] = my_div["a_tag_href"]
                event_list.append(event)

        self.events = pd.DataFrame(event_list, columns=['title', 'link_detail'])


    def save_events(self):
        temp_file = f"tmp_crawler_event_page_{self.current_page}.json"

        print(f"{self.temp_path}/{temp_file}")
        self.events.to_json(f"{self.temp_path}/{temp_file}")


    def is_finished(self):

        if not self.started:
            return False

        if self.current_page < self.limit_page:
            return False
        
        else:
            return True
        

    def next_page(self):
        self.current_page += 1


class SymplaCrawlerEventDetail:
    def __init__(self, event_url):
        self.event_url = event_url
    

    def get_event_detail(self):
        from core.requests import RequestApi
        request = RequestApi()

        response = request.get_endpoint(self.event_url)

        soup = BeautifulSoup(response.text, 'html.parser')

        divs = soup.find_all("div")
        div_list = []

        for div in divs:
            div_dict = {}

            try:
                id = div["id"]
                div_dict["id"] = id

            except Exception as e:
                div_dict["id"] = ["NA"]

            try:
                classes_name = div["class"]
                div_dict["classes_name"] = classes_name

            except Exception as e:
                div_dict["classes_name"] = ["NA"]


            try:
                classes_text = div.text
                div_dict["classes_text"] = classes_text

            except Exception as e:
                div_dict["classes_text"] = ["NA"]


            div_list.append(div_dict)

        print(div_list)

        self.event = {}

        for my_div in div_list:
            classes_name = my_div["classes_name"]
            calendar_criterial = "event-info-calendar"
            calendar_criterial_list = list(filter(lambda item: calendar_criterial in item, classes_name))

            city_criterial = "event-info-city"
            city_criterial_list = list(filter(lambda item: city_criterial in item, classes_name))


            if calendar_criterial_list:
                self.event["calendar"] = my_div["classes_text"]
                # event_list.append(event)

            if city_criterial_list:
                self.event["city"] = my_div["classes_text"]
                # event_list.append(event)

        print(self.event)