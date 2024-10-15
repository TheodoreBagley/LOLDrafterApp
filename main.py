import requests
from bs4 import BeautifulSoup
champs_list = []

url = 'https://www.counterstats.net/'

response = requests.get(url)

if response.status_code == 200:

    soup = BeautifulSoup(response.content, 'html.parser')
    #print(soup.prettify()[:100000])

    champion_divs = soup.find_all('div', class_='champion-icon champList')

    #champs_list = []

    for div in champion_divs:
        champion_id = div.get('id')
        if champion_id:
            #print(champion_id)
            if '-' in champion_id:
                champion_id = champion_id.replace('-', '')
                print(champion_id)
            if "nunu" in champion_id:
                champion_id = "nunu"
            champs_list.append(champion_id.strip())

    #print(champs_list)
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")




# TODO: https://lolalytics.com/lol/<champ i>/vs/<champ j>/build/?tier=master_plus


for champ in champs_list:
    for enemy in champs_list:
        new_url =  'https://lolalytics.com/lol/' + champ + '/vs/' + enemy + '/build/?tier=master_plus'
        #print(new_url)
        data = response = requests.get(url)
        soupy = BeautifulSoup(data.content, 'html.parser')
        para = soupy.find('div', attrs={'q:key': 'yJ_1'})
        print(para)