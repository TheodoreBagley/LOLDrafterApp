import requests
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import io
import json

with open('champions_data.json', 'r') as f:
    champions_data = json.load(f)

champion_names = [champion['name'] for champion in champions_data['data'].values()]

def show_champion_details(event):
    selected_champion = champion_combo.get()
    champion_info = next((champion for champion in champions_data.values() if champion['name'] == selected_champion), None)
    if champion_info:
        details_label.config(text=f"Name: {champion_info['name']}\nTags: {', '.join(champion_info['tags'])}\nTitle: {champion_info['title']}")
        
        # Load and display champion image
        image_url = f"https://ddragon.leagueoflegends.com/cdn/14.20.1/img/champion/{champion_info['image']['full']}"
        image_response = requests.get(image_url)
        
        if image_response.status_code == 200:
            # Open the image
            image_data = Image.open(io.BytesIO(image_response.content))
            image = ImageTk.PhotoImage(image_data)
            
            # Update the image label
            image_label.config(image=image)
            image_label.image = image  # Keep a reference to avoid garbage collection
        else:
            print(f"Error fetching image: {image_response.status_code} - {image_response.text}")

# Create the main window
root = tk.Tk()
root.title("League of Legends Champion Selector")

# Create a dropdown menu
champion_combo = ttk.Combobox(root, values=champion_names)
champion_combo.set("Select a Champion")  # Default text
champion_combo.bind("<<ComboboxSelected>>", show_champion_details)
champion_combo.pack(pady=10)

# Create a label to show champion details
details_label = tk.Label(root, text="", justify=tk.LEFT)
details_label.pack(pady=10)

# Create an image label
image_label = tk.Label(root)
image_label.pack(pady=10)

# Run the application
root.mainloop()