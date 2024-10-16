import re

import requests
from bs4 import BeautifulSoup

class Champion:
    def __init__(self, name: str, lanes: list):
        self.name = name
        self.lanes = lanes

    def __repr__(self):
        return f"Champion(name='{self.name}', lanes={self.lanes})"


champs_list = []

url = 'https://www.counterstats.net/'

response = requests.get(url)

if response.status_code == 200:

    soup = BeautifulSoup(response.content, 'html.parser')


    champion_divs = soup.find_all('div', class_='champion-icon champList')

    #champs_list = []

    for div in champion_divs:
        champion_name = div.get('id')
        if champion_name:
            #print(champion_id)
            if '-' in champion_name:
                champion_id = champion_name.replace('-', '')
                print(champion_id)
            if "nunu" in champion_name:
                champion_id = "nunu"
            #champs_list.append(champion_id.strip())
        champion_lanes = div.get('data-lanes')
        lanes = re.findall(r'jungle|top|mid|adc|support', champion_lanes)
        champs_list.append(Champion(champion_name, lanes))
    for champ in champs_list:
        print(champ)
    #print(champs_list)
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")




# TODO: https://www.counterstats.net/league-of-legends/


for champ in champs_list:
    for enemy in champs_list:
        if enemy.lanes[0] == champ.lanes[0]:
            new_url =  'https://www.counterstats.net/league-of-legends/' + champ.name + '/vs-' + enemy.name + '/' + champ.lanes[0] + '/all'
        else:
            continue
        #print(new_url)
        response = requests.get(new_url)

        if response.status_code == 200:
            print(new_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            with open('output.txt', 'w', encoding='utf-8') as file:
                file.write(new_url)

            span_elements = soup.find_all('span', attrs={'data-perc': True})
            print(span_elements)
            if span_elements:
                span_element = span_elements[6]
            else:
                continue
            if span_element:
                data_perc = span_element['data-perc']
                print(data_perc)
            else:

                print("Element not found")

