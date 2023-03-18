# # from ingestor.crawler.sympla import SymplaCrawlerEventDetail
# from bs4 import BeautifulSoup

# url = "https://www.sympla.com.br/evento-online/encanador-fazenda-rio-grande/813865"
# # sympla_crawler_detail = SymplaCrawlerEventDetail(url)

# from core.requests import RequestApi

# request = RequestApi()

# # self.__mount_url()
# # self.started = True

# response = request.get_endpoint(url)

# soup = BeautifulSoup(response.text, 'html.parser')

# divs = soup.find_all("div")
# div_list = []
# for div in divs:
#     div_dict = {}

#     try:
#         classes_name = div["class"]
#         div_dict["classes_name"] = classes_name

#     except Exception as e:
#         div_dict["classes_name"] = ["NA"]


#     try:
#         classes_text = div.text
#         div_dict["classes_text"] = classes_text

#     except Exception as e:
#         div_dict["classes_text"] = ["NA"]


#     div_list.append(div_dict)

# event = {}

# for my_div in div_list:
#     classes_name = my_div["classes_name"]
#     calendar_criterial = "event-info-calendar"
#     calendar_criterial_list = list(filter(lambda item: calendar_criterial in item, classes_name))

#     city_criterial = "event-info-city"
#     city_criterial_list = list(filter(lambda item: city_criterial in item, classes_name))


#     if calendar_criterial_list:
#         event["calendar"] = my_div["classes_text"]
#         # event_list.append(event)

#     if city_criterial_list:
#         event["city"] = my_div["classes_text"]
#         # event_list.append(event)

# print(event)



from ingestor.crawler.sympla import SymplaCrawlerEventDetail
import pandas as pd

df = pd.read_json("/opt/airflow/logs/tmp_crawler_event_page_1.json")

print(df)

for index, row in df.iterrows():
    title = row['title']
    link = row['link_detail']
    print(f'{title} - {link}')
    sympla_crawler_detail = SymplaCrawlerEventDetail(link)    
    sympla_crawler_detail.get_event_detail()
    f = input("Compare")

# url = "https://www.sympla.com.br/evento-online/encanador-fazenda-rio-grande/813865"

# sympla_crawler_detail = SymplaCrawlerEventDetail(url)

# sympla_crawler_detail.get_event_detail()

