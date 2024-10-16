import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import json

# Load champion data from JSON file
with open('champions_data.json', 'r') as f:
    champions_data = json.load(f)['data']

champion_names = [champion['name'] for champion in champions_data.values()]

def show_champion_details(event):
    selected_champion = champion_combo.get()
    champion_info = next((champion for champion in champions_data.values() if champion['name'] == selected_champion), None)
    if champion_info:
        details_label.config(text=f"Name: {champion_info['name']}\nTags: {', '.join(champion_info['tags'])}\nTitle: {champion_info['title']}")
        
        image_filename = champion_info['image']['full']
        image_path = os.path.join('champion_images', image_filename)
        
        if os.path.exists(image_path):
            # Load image if it exists in cache
            image_data = Image.open(image_path)
            image_data = image_data.resize((200, 200), Image.ANTIALIAS)  # Resize for better fit
            image = ImageTk.PhotoImage(image_data)
            image_label.config(image=image)
            image_label.image = image  # Keep a reference to avoid garbage collection
        else:
            print(f"Image not found in cache: {image_path}")
            return  # Exit if the image could not be found

# Create the main window
root = tk.Tk()
root.title("League of Legends Champion Selector")
root.geometry("600x600")  # Set the size of the window

# Create a frame for better organization
frame = tk.Frame(root)
frame.pack(pady=20)

# Create a dropdown menu
champion_combo = ttk.Combobox(frame, values=champion_names, font=("Arial", 12), width=30)
champion_combo.set("Select a Champion")  # Default text
champion_combo.bind("<<ComboboxSelected>>", show_champion_details)
champion_combo.pack(pady=10)

# Create a label to show champion details
details_label = tk.Label(frame, text="", justify=tk.LEFT, font=("Arial", 12))
details_label.pack(pady=10)

# Create an image label
image_label = tk.Label(frame)
image_label.pack(pady=10)

# Run the application
root.mainloop()
