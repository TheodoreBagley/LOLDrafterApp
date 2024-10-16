import requests
import json
import os
from collections import defaultdict
from PIL import Image


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

    return champions_data['data']

def get_champion_names(champ_data):
    return [champion['name'] for champion in champ_data.values()]

def group_champs_by_tag(champ_data):
    champions_by_tags = defaultdict(list)

    # Group champions by their tags
    for champion in champ_data.values():
        for tag in champion['tags']:
            champions_by_tags[tag].append(champion['name'])

    # Convert defaultdict to a regular dict for better readability
    champions_by_tags = dict(champions_by_tags)

    # Print the champions grouped by tags
    for tag, champions in champions_by_tags.items():
        print(f"{tag}: {', '.join(champions)}")

# Check if the file already exists
if os.path.exists(file_path):
    # Load data from the file
    with open(file_path, 'r') as f:
        champions_data = json.load(f)['data']
else:
    # Fetch data from API and store it locally
    champions_data = fetch_champion_data()

group_champs_by_tag(champions_data)
# Extract champion names
champion_names = get_champion_names(champions_data)

#print(champion_names)  # Print the list of champion names

def get_champion_images(champ_data):
    cache_dir = "champion_images"
    os.makedirs(cache_dir, exist_ok=True)

    for champ in champ_data.values():
        image_filename = champ['image']['full']
        image_path = os.path.join(cache_dir, image_filename)
        image_url = f"https://ddragon.leagueoflegends.com/cdn/14.20.1/img/champion/{champ['image']['full']}"
        image_response = requests.get(image_url)
        with open(image_path, 'wb') as img_file:
            img_file.write(image_response.content)
    



