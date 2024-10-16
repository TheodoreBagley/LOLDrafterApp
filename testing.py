import requests
import json
import os
from collections import defaultdict

# File path to store the champion data
file_path = "champions_data.json"

def fetch_champion_data():
    # Step 1: Get the latest version
    version_url = "https://ddragon.leagueoflegends.com/api/versions.json"
    response = requests.get(version_url)
    latest_version = response.json()[0]  # First element is the latest version

    # Step 2: Get the list of champions for the latest version
    champion_url = f"https://ddragon.leagueoflegends.com/cdn/{latest_version}/data/en_US/champion.json"
    champion_response = requests.get(champion_url)
    champions_data = champion_response.json()

    # Save data to a local file
    with open(file_path, 'w') as f:
        json.dump(champions_data, f)

    return champions_data

def get_champion_names(champ_data):
    return [champion['name'] for champion in champ_data['data'].values()]

# Check if the file already exists
if os.path.exists(file_path):
    # Load data from the file
    with open(file_path, 'r') as f:
        champions_data = json.load(f)
else:
    # Fetch data from API and store it locally
    champions_data = fetch_champion_data()


def get_tags(champ_data):
    pot_tags = set()
    for c in champ_data['data'].values():
        for tag in c['tags']:
            pot_tags.add(tag)
    return list(pot_tags)

def group_champs_by_tag(champ_data):
    champions_by_tags = defaultdict(list)

    # Group champions by their tags
    for champion in champions_data['data'].values():
        for tag in champion['tags']:
            champions_by_tags[tag].append(champion['name'])

    # Convert defaultdict to a regular dict for better readability
    champions_by_tags = dict(champions_by_tags)

    # Print the champions grouped by tags
    for tag, champions in champions_by_tags.items():
        print(f"{tag}: {', '.join(champions)}")

print(get_tags(champions_data))
group_champs_by_tag(champions_data)
# Extract champion names
champion_names = get_champion_names(champions_data)

#print(champion_names)  # Print the list of champion names




