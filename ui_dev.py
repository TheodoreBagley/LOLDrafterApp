import json
import tkinter as tk
from tkinter import ttk

with open('champions_data.json', 'r') as f:
    champions_data = json.load(f)

champion_names = [champion['name'] for champion in champions_data['data'].values()]

# Function to show selected champion details
def show_champion_details(event):
    selected_champion = champion_combo.get()
    champion_info = next((champion for champion in champions_data['data'].values() if champion['name'] == selected_champion), None)
    if champion_info:
        details_label.config(text=f"Name: {champion_info['name']}\nTags: {', '.join(champion_info['tags'])}\nLore: {champion_info['lore']}")

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

# Run the application
root.mainloop()