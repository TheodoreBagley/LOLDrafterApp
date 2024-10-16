import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import json

# Load champion data from JSON file
with open('champions_data.json', 'r') as f:
    champions_data = json.load(f)['data']

champion_names = [champion['name'] for champion in champions_data.values()]
num_columns = 10  # Specify the number of columns for the layout

def show_champion_details(champion_name):
    champion_info = next((champion for champion in champions_data.values() if champion['name'] == champion_name), None)
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
root.geometry("1450x800")  # Set the size of the window

# Create a canvas and a scrollbar
canvas = tk.Canvas(root)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

# Configure the canvas
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Pack the canvas and scrollbar
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Load and display champion images
for index, champion in enumerate(champions_data.values()):
    image_filename = champion['image']['full']
    image_path = os.path.join('champion_images', image_filename)

    if os.path.exists(image_path):
        image_data = Image.open(image_path)
        image_data = image_data.resize((100, 100), Image.ANTIALIAS)  # Resize for uniformity
        image = ImageTk.PhotoImage(image_data)

        # Create a button with the champion image
        button = tk.Button(scrollable_frame, image=image, command=lambda name=champion['name']: show_champion_details(name))
        button.image = image  # Keep a reference

        # Calculate row and column for grid layout
        row = index // num_columns
        column = index % num_columns
        button.grid(row=row, column=column, padx=5, pady=5)  # Adjust grid layout

# Create a label to show champion details
details_label = tk.Label(root, text="", justify=tk.LEFT, font=("Arial", 12))
details_label.pack(pady=10)

# Create an image label for displaying the selected champion's larger image
image_label = tk.Label(root)
image_label.pack(pady=10)

# Run the application
root.mainloop()
