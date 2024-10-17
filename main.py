import json
import re
import requests
from bs4 import BeautifulSoup
from peewee import *

class Champion:
    def __init__(self, name: str, winPercent: float, lanes: list, winrate: dict):
        self.name = name
        self.winPercent = winPercent
        self.lanes = lanes
        self.winrate = winrate

    def __repr__(self):
        return f"Champion(name='{self.name}', winPercent='{self.winPercent}', lanes={self.lanes}, winrate={self.winrate})"

    def update_winrate(self, enemy: str, rate: float):
        self.winrate[enemy] = rate


champs_list = []

url = 'https://www.counterstats.net/'

response = requests.get(url)

if response.status_code == 200:

    soup = BeautifulSoup(response.content, 'html.parser')


    champion_divs = soup.find_all('div', class_='champion-icon champList')

    #champs_list = []

    for div in champion_divs:
        #get champ names
        champion_name = div.get('id')
        if champion_name:
            #print(champion_id)
            if '-' in champion_name:
                champion_id = champion_name.replace('-', '')
                print(champion_id)
            if "nunu" in champion_name:
                champion_id = "nunu"

        #get champ lanes
        champion_lanes = div.get('data-lanes')
        lanes = re.findall(r'jungle|top|mid|adc|support', champion_lanes)

        #get overall win rate
        champion_wins = float(div.get('data-winrate'))
        champs_list.append(Champion(champion_name, champion_wins, lanes, {}))
    for champ in champs_list:
        print(champ)
    #print(champs_list)
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")



for champ in champs_list:
    for enemy in champs_list:
        #only look at champs in same role
        if enemy.lanes[0] == champ.lanes[0]:
            new_url =  'https://www.counterstats.net/league-of-legends/' + champ.name + '/vs-' + enemy.name + '/' + champ.lanes[0] + '/all'
        else:
            continue
        #don't compare champs to themself
        if champ.name == enemy.name:
            continue

        response = requests.get(new_url)
        if response.status_code == 200:
            #print(new_url)
            soup = BeautifulSoup(response.content, 'html.parser')

            span_elements = soup.find_all('span', attrs={'data-perc': True})
            #print(span_elements)
            #get the winrate element
            if span_elements:
                span_element = span_elements[6]
            else:
                continue
            if span_element:
                data_perc = span_element['data-perc']
                champ.update_winrate(enemy.name, data_perc)
                print(data_perc)
            else:
                pass
                #print("Element not found")

for champ in champs_list:
    print(champ)


db = SqliteDatabase('champions.db')

class Champions(Model):
    name = CharField(unique=True)
    totalWinRate = FloatField()
    lanes = TextField()
    winrate = TextField()

    class Meta:
        database = db


db.connect()
db.create_tables([Champions])
for champ in champs_list:
    champion_data = {
        'name': champ.name,
        'totalWinRate': champ.winPercent,
        'lanes': champ.lanes,
        'winrate': json.dumps(champ.winrate)
    }
    Champions.create(**champion_data)
    print(champ.name + " added")
