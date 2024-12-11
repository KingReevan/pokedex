# Importing of all files
import tkinter as tk  # For the GUI
from tkinter import ttk, messagebox  # More modern appearance
import joblib  # For paralled Processing, pipelining, handles large amounts of data in numpy arrays
import pandas as pd  # Data Manipulation
import plotly.express as px  # Main data Visualization Tool
import plotly.graph_objects as go  # For creating various plots
from PIL import ImageTk, Image  # To import and display images
import urllib.request  # To fetch URL
from io import BytesIO  # Memory management for image data
import requests  # API that allows to send HTTP requests
import numpy as np  # Array Manipulation and Scientific Computing

from train_model import calculate_type_advantage

# Display options to show all rows and columns
pd.set_option('display.max_rows', None)  # Shows all rows
pd.set_option('display.max_columns', None)  # Shows all columns
pd.set_option('display.width', 1000)  # Display width
pd.set_option('display.max_colwidth', None)  # Shows full content of each cell

# Load the pokemon_updated excel file into the project and pandas will convert it into a readable data frame
file_path = r"C:\Users\reeva\Music\pokemon_updated.xlsx"  # File path of pokemon_updated.xlsx
df = pd.read_excel(file_path)

#The following is for type matchups, 'super effective' types will do double damage and 'Not very effective' will do half the damage. This may change depending on the region.
type_matchup = {
    'Normal': {'Normal': 1.0, 'Fire': 1.0, 'Water': 1.0, 'Electric': 1.0, 'Grass': 1.0, 'Ice': 1.0, 'Fighting': 1.0, 'Poison': 1.0, 'Ground': 1.0, 'Flying': 1.0, 'Psychic': 1.0, 'Bug': 1.0, 'Rock': 0.5, 'Ghost': 0, 'Dragon': 1.0, 'Dark': 1.0, 'Steel': 0.5, 'Fairy': 1.0},
    'Fire': {'Normal': 1.0, 'Fire': 0.5, 'Water': 0.5, 'Electric': 1.0, 'Grass': 2.0, 'Ice': 2.0, 'Fighting': 1.0, 'Poison': 1.0, 'Ground': 1.0, 'Flying': 1.0, 'Psychic': 1.0, 'Bug': 2.0, 'Rock': 0.5, 'Ghost': 1.0, 'Dragon': 0.5, 'Dark': 1.0, 'Steel': 2.0, 'Fairy': 1.0},
    'Water': {'Normal': 1.0, 'Fire': 2.0, 'Water': 0.5, 'Electric': 1.0, 'Grass': 0.5, 'Ice': 1.0, 'Fighting': 1.0, 'Poison': 1.0, 'Ground': 2.0, 'Flying': 1.0, 'Psychic': 1.0, 'Bug': 1.0, 'Rock': 2.0, 'Ghost': 1.0, 'Dragon': 0.5, 'Dark': 1.0, 'Steel': 1.0, 'Fairy': 1.0},
    'Electric': {'Normal': 1.0, 'Fire': 1.0, 'Water': 2.0, 'Electric': 0.5, 'Grass': 0.5, 'Ice': 1.0, 'Fighting': 1.0, 'Poison': 1.0, 'Ground': 0, 'Flying': 2.0, 'Psychic': 1.0, 'Bug': 1.0, 'Rock': 1.0, 'Ghost': 1.0, 'Dragon': 0.5, 'Dark': 1.0, 'Steel': 1.0, 'Fairy': 1.0},
    'Grass': {'Normal': 1.0, 'Fire': 0.5, 'Water': 2.0, 'Electric': 1.0, 'Grass': 0.5, 'Ice': 1.0, 'Fighting': 1.0, 'Poison': 0.5, 'Ground': 2.0, 'Flying': 0.5, 'Psychic': 1.0, 'Bug': 0.5, 'Rock': 2.0, 'Ghost': 1.0, 'Dragon': 0.5, 'Dark': 1.0, 'Steel': 0.5, 'Fairy': 1.0},
    'Ice': {'Normal': 1.0, 'Fire': 0.5, 'Water': 0.5, 'Electric': 1.0, 'Grass': 2.0, 'Ice': 0.5, 'Fighting': 1.0, 'Poison': 1.0, 'Ground': 2.0, 'Flying': 2.0, 'Psychic': 1.0, 'Bug': 1.0, 'Rock': 1.0, 'Ghost': 1.0, 'Dragon': 2.0, 'Dark': 1.0, 'Steel': 0.5, 'Fairy': 1.0},
    'Fighting': {'Normal': 2.0, 'Fire': 1.0, 'Water': 1.0, 'Electric': 1.0, 'Grass': 1.0, 'Ice': 2.0, 'Fighting': 1.0, 'Poison': 0.5, 'Ground': 1.0, 'Flying': 0.5, 'Psychic': 0.5, 'Bug': 0.5, 'Rock': 2.0, 'Ghost': 0, 'Dragon': 1.0, 'Dark': 2.0, 'Steel': 2.0, 'Fairy': 0.5},
    'Poison': {'Normal': 1.0, 'Fire': 1.0, 'Water': 1.0, 'Electric': 1.0, 'Grass': 2.0, 'Ice': 1.0, 'Fighting': 1.0, 'Poison': 0.5, 'Ground': 0.5, 'Flying': 1.0, 'Psychic': 1.0, 'Bug': 1.0, 'Rock': 0.5, 'Ghost': 0.5, 'Dragon': 1.0, 'Dark': 1.0, 'Steel': 0, 'Fairy': 2.0},
    'Ground': {'Normal': 1.0, 'Fire': 2.0, 'Water': 1.0, 'Electric': 2.0, 'Grass': 0.5, 'Ice': 1.0, 'Fighting': 1.0, 'Poison': 2.0, 'Ground': 1.0, 'Flying': 0, 'Psychic': 1.0, 'Bug': 0.5, 'Rock': 2.0, 'Ghost': 1.0, 'Dragon': 1.0, 'Dark': 1.0, 'Steel': 2.0, 'Fairy': 1.0},
    'Flying': {'Normal': 1.0, 'Fire': 1.0, 'Water': 1.0, 'Electric': 0.5, 'Grass': 2.0, 'Ice': 1.0, 'Fighting': 2.0, 'Poison': 1.0, 'Ground': 1.0, 'Flying': 1.0, 'Psychic': 1.0, 'Bug': 2.0, 'Rock': 0.5, 'Ghost': 1.0, 'Dragon': 1.0, 'Dark': 1.0, 'Steel': 0.5, 'Fairy': 1.0},
    'Psychic': {'Normal': 1.0, 'Fire': 1.0, 'Water': 1.0, 'Electric': 1.0, 'Grass': 1.0, 'Ice': 1.0, 'Fighting': 2.0, 'Poison': 2.0, 'Ground': 1.0, 'Flying': 1.0, 'Psychic': 0.5, 'Bug': 1.0, 'Rock': 1.0, 'Ghost': 1.0, 'Dragon': 1.0, 'Dark': 0, 'Steel': 0.5, 'Fairy': 1.0},
    'Bug': {'Normal': 1.0, 'Fire': 0.5, 'Water': 1.0, 'Electric': 1.0, 'Grass': 2.0, 'Ice': 1.0, 'Fighting': 0.5, 'Poison': 0.5, 'Ground': 1.0, 'Flying': 0.5, 'Psychic': 2.0, 'Bug': 1.0, 'Rock': 1.0, 'Ghost': 0.5, 'Dragon': 1.0, 'Dark': 2.0, 'Steel': 0.5, 'Fairy': 0.5},
    'Rock': {'Normal': 1.0, 'Fire': 2.0, 'Water': 1.0, 'Electric': 1.0, 'Grass': 1.0, 'Ice': 2.0, 'Fighting': 0.5, 'Poison': 1.0, 'Ground': 0.5, 'Flying': 2.0, 'Psychic': 1.0, 'Bug': 2.0, 'Rock': 1.0, 'Ghost': 1.0, 'Dragon': 1.0, 'Dark': 1.0, 'Steel': 0.5, 'Fairy': 1.0},
    'Ghost': {'Normal': 0, 'Fire': 1.0, 'Water': 1.0, 'Electric': 1.0, 'Grass': 1.0, 'Ice': 1.0, 'Fighting': 1.0, 'Poison': 1.0, 'Ground': 1.0, 'Flying': 1.0, 'Psychic': 2.0, 'Bug': 1.0, 'Rock': 1.0, 'Ghost': 2.0, 'Dragon': 1.0, 'Dark': 0.5, 'Steel': 1.0, 'Fairy': 1.0},
    'Dragon': {'Normal': 1.0, 'Fire': 1.0, 'Water': 1.0, 'Electric': 1.0, 'Grass': 1.0, 'Ice': 1.0, 'Fighting': 1.0, 'Poison': 1.0, 'Ground': 1.0, 'Flying': 1.0, 'Psychic': 1.0, 'Bug': 1.0, 'Rock': 1.0, 'Ghost': 1.0, 'Dragon': 2.0, 'Dark': 1.0, 'Steel': 0.5, 'Fairy': 0},
    'Dark': {'Normal': 1.0, 'Fire': 1.0, 'Water': 1.0, 'Electric': 1.0, 'Grass': 1.0, 'Ice': 1.0, 'Fighting': 0.5, 'Poison': 1.0, 'Ground': 1.0, 'Flying': 1.0, 'Psychic': 2.0, 'Bug': 1.0, 'Rock': 1.0, 'Ghost': 2.0, 'Dragon': 1.0, 'Dark': 0.5, 'Steel': 1.0, 'Fairy': 0.5},
    'Steel': {'Normal': 1.0, 'Fire': 0.5, 'Water': 0.5, 'Electric': 0.5, 'Grass': 1.0, 'Ice': 2.0, 'Fighting': 1.0, 'Poison': 1.0, 'Ground': 1.0, 'Flying': 1.0, 'Psychic': 1.0, 'Bug': 1.0, 'Rock': 2.0, 'Ghost': 1.0, 'Dragon': 1.0, 'Dark': 1.0, 'Steel': 0.5, 'Fairy': 2.0},
    'Fairy': {'Normal': 1.0, 'Fire': 0.5, 'Water': 1.0, 'Electric': 1.0, 'Grass': 1.0, 'Ice': 1.0, 'Fighting': 2.0, 'Poison': 0.5, 'Ground': 1.0, 'Flying': 1.0, 'Psychic': 1.0, 'Bug': 1.0, 'Rock': 1.0, 'Ghost': 1.0, 'Dragon': 2.0, 'Dark': 2.0, 'Steel': 0.5, 'Fairy': 1.0}
}

# This is where the GUI implementation will take place
class PokemonDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Pokémon Statistics Visualization Dashboard")    # Title of the window
        self.root.geometry("1400x1000")            # Dimensions of the window
        self.root.configure(bg="#9593D9")     # Main Background Color

        # Styling for all the buttons
        style = ttk.Style()
        style.configure("TButton", font=("Montserrat SemiBold", 12, "bold"), foreground="#291528", background="#E63462",
                        padding=10)
        style.map("TButton",
                  foreground=[("pressed", "#7C90DB"), ("active", "#E63462")],
                  background=[("pressed", "!disabled", "#ff66b2"), ("active", "#ff66b2")])

        style.configure("Custom.TLabel", font=("Montserrat SemiBold", 14), foreground="white",
                        background="#E63462")  # Styling for the 'Show Pokemon Stats' button
        button_width = 30  # The fixed width for all buttons

        # Specific style for the spider plot
        spider_style = ttk.Style()
        spider_style.configure("SpiderButton.TButton", font=("Montserrat SemiBold", 12, "bold"),
                               foreground="#291528", background="#4CAF50", padding=10)

        # Spider Plot's active and pressed state colors
        spider_style.map("SpiderButton.TButton",
                         foreground=[("pressed", "#ECCE8E"), ("active", "#ECCE8E")],
                         background=[("pressed", "!disabled", "#388E3C"), ("active", "#ECCE8E")])

        # Generation Selector
        ttk.Label(root, text="Select Generation:", style="Custom.TLabel").grid(row=0, column=0, padx=10, pady=10)
        self.gen_var = tk.IntVar(value=1)  # Keeping generation 1 as the default generation (Kanto region)
        gen_options = list(df['Generation'].unique())  # Creates a list object with each generation included
        self.gen_select = ttk.Combobox(root, textvariable=self.gen_var, values=gen_options, state="readonly", width=40)  #Creates a drop-down menu with all the generations included
        self.gen_select.grid(row=0, column=1, padx=10, pady=10)    # Position of the menu in the grid

        # Every single button definition
        self.scatter_button = ttk.Button(root, text="Attack VS Defense", command=self.show_scatter, width=button_width)
        self.scatter_button.grid(row=1, column=0, padx=10, pady=10)

        self.box_button = ttk.Button(root, text="Generation Combat Statistics", command=self.show_box_plot,
                                     width=button_width)
        self.box_button.grid(row=1, column=1, padx=10, pady=10)

        self.bar_button = ttk.Button(root, text="Average Stats For Each Type", command=self.show_bar_plot,
                                     width=button_width)
        self.bar_button.grid(row=1, column=2, padx=10, pady=10)

        self.histogram_button_HP = ttk.Button(root, text="HP Distribution", command=self.show_histogram_HP,
                                              width=button_width)
        self.histogram_button_HP.grid(row=2, column=0, padx=10, pady=10)

        self.histogram_button_Attack = ttk.Button(root, text="Attack Distribution", command=self.show_histogram_Attack,
                                                  width=button_width)
        self.histogram_button_Attack.grid(row=2, column=1, padx=10, pady=10)

        self.histogram_button_Defense = ttk.Button(root, text="Defense Distribution",
                                                   command=self.show_histogram_Defense, width=button_width)
        self.histogram_button_Defense.grid(row=2, column=2, padx=10, pady=10)

        self.histogram_button_SpAtk = ttk.Button(root, text="Special Attack Distribution",
                                                 command=self.show_histogram_SPAttack, width=button_width)
        self.histogram_button_SpAtk.grid(row=3, column=0, padx=10, pady=10)

        self.histogram_button_SpDef = ttk.Button(root, text="Special Defense Distribution",
                                                 command=self.show_histogram_SPDefense, width=button_width)
        self.histogram_button_SpDef.grid(row=3, column=1, padx=10, pady=10)

        self.histogram_button_Speed = ttk.Button(root, text="Speed Distribution", command=self.show_histogram_Speed,
                                                 width=button_width)
        self.histogram_button_Speed.grid(row=3, column=2, padx=10, pady=10)

        self.compare_button = ttk.Button(root, text="Compare Two Pokemon", command=self.open_comparison_page,
                                         width=button_width)
        self.compare_button.grid(row=4, column=0, padx=10, pady=10)

        self.best_button = ttk.Button(root, text="Best Pokemon For Each Statistic",
                                      command=self.show_best_pokemon_for_each_stat, width=button_width)
        self.best_button.grid(row=4, column=1, padx=10, pady=10)

        self.scatter_button_Special = ttk.Button(root, text="Sp. Attack VS Sp. Defense",
                                                 command=self.show_scatter_special, width=button_width)
        self.scatter_button_Special.grid(row=4, column=2, padx=10, pady=10)

        self.legendary_button = ttk.Button(root, text="Legendary Pokemon", command=self.show_legendary_pokemon_window,
                                           width=button_width)
        self.legendary_button.grid(row=5, column=1, padx=10, pady=10)

        self.secondary_type = ttk.Button(root, text="Secondary Type Distribution",
                                         command=self.show_secondary_type_distribution, width=button_width)
        self.secondary_type.grid(row=5, column=0, padx=10, pady=10)

        self.most_powerful = ttk.Button(root, text="Top 10 most powerful pokemon",
                                        command=self.show_top_10_powerful_pokemon, width=button_width)
        self.most_powerful.grid(row=5, column=2, padx=10, pady=10)

        # To view stats for an individual pokemon by providing the pokedex number
        ttk.Label(root, text="Enter Pokédex Number: ", style="Custom.TLabel").grid(row=6, column=0, padx=10, pady=10)  # Label to prompt user to enter a pokedex number
        self.pokemon_num = tk.StringVar()
        self.num_entry = ttk.Entry(root, textvariable=self.pokemon_num, width=40)
        self.num_entry.grid(row=6, column=1, padx=10, pady=10)
        self.spider_button = ttk.Button(root, text="Show Pokémon Stats", command=self.show_spider_plot,
                                        width=button_width, style="SpiderButton.TButton")      # Button to activate spider plot
        self.spider_button.grid(row=6, column=2, padx=10, pady=10)
        self.spider_button = ttk.Button(root, text="Show Pokémon Stats", command=self.show_spider_plot,
                                        width=button_width, style="SpiderButton.TButton")

        self.predict_button = ttk.Button(self.root, text="Prediction", command=self.open_prediction_window, width=button_width) # The button for prediction
        self.predict_button.grid(row=0, column=2, padx=10, pady=10)

        # Placeholder for Pokémon image
        self.image_label = tk.Label(self.root)
        self.image_label.grid(row=8, column=2, columnspan=1, pady=10)



    # Scatter plot to show Attack VS Defense graph for each pokemon in the selected generation
    def show_scatter(self):
        generation = self.gen_var.get()
        filtered_df = df[df['Generation'] == generation]
        fig = px.scatter(filtered_df, x='Attack', y='Defense', color='Type 1',
                         hover_data=['Name'], title=f'Attack vs Defense for Generation {generation}')
        fig.show()

    # Scatter plot to show Sp. Attack VS Sp. Defense for each pokemon in the selected generation
    def show_scatter_special(self):
        generation = self.gen_var.get()
        filtered_df = df[df['Generation'] == generation]
        fig = px.scatter(filtered_df, x='Sp. Atk', y='Sp. Def', color='Type 1',
                         hover_data=['Name'], title=f'Special Attack vs Special Defense for Generation {generation}')
        fig.show()

    # Histogram to show HP distribution for the selected generation
    def show_histogram_HP(self):
        generation = self.gen_var.get()
        filtered_df = df[df['Generation'] == generation]
        fig = px.histogram(filtered_df, x='HP', nbins=20, color='Type 1',
                           title=f'HP Distribution for Generation {generation}')
        fig.show()

    # Histogram to show Attack distribution for the selected generation
    def show_histogram_Attack(self):
        generation = self.gen_var.get()
        filtered_df = df[df['Generation'] == generation]
        fig = px.histogram(filtered_df, x='Attack', nbins=20, color='Type 1',
                           title=f'Attack Distribution for Generation {generation}')
        fig.show()

    # Histogram to show Defense distribution for the selected generation
    def show_histogram_Defense(self):
        generation = self.gen_var.get()
        filtered_df = df[df['Generation'] == generation]
        fig = px.histogram(filtered_df, x='Defense', nbins=20, color='Type 1',
                           title=f'Defense Distribution for Generation {generation}')
        fig.show()

    # Histogram to show Sp. Attack distribution for the selected generation
    def show_histogram_SPAttack(self):
        generation = self.gen_var.get()
        filtered_df = df[df['Generation'] == generation]
        fig = px.histogram(filtered_df, x='Sp. Atk', nbins=20, color='Type 1',
                           title=f'Special Attack Distribution for Generation {generation}')
        fig.show()

    # Histogram to show Sp. Defense distribution for the selected generation
    def show_histogram_SPDefense(self):
        generation = self.gen_var.get()
        filtered_df = df[df['Generation'] == generation]
        fig = px.histogram(filtered_df, x='Sp. Def', nbins=20, color='Type 1',
                           title=f'Special Defense Distribution for Generation {generation}')
        fig.show()

    # Histogram to show Speed distribution for the selected generation
    def show_histogram_Speed(self):
        generation = self.gen_var.get()
        filtered_df = df[df['Generation'] == generation]
        fig = px.histogram(filtered_df, x='Speed', nbins=20, color='Type 1',
                           title=f'Speed Distribution for Generation {generation}')
        fig.show()

    # Box plot to see how the stats compare to each other for a generation
    def show_box_plot(self):
        generation = self.gen_var.get()
        filtered_df = df[df['Generation'] == generation]
        fig = px.box(filtered_df, y=['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed'],
                     title=f'Stats Comparison for Generation {generation}')
        fig.show()

    # Bar Plot to show the average stats for a generation for all of the 18 types
    def show_bar_plot(self):
        generation = self.gen_var.get()
        filtered_df = df[df['Generation'] == generation]
        numeric_columns = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']
        avg_stats_by_type = filtered_df.groupby('Type 1')[numeric_columns].mean().reset_index()
        fig = px.bar(avg_stats_by_type, x='Type 1', y=numeric_columns,
                     title=f'Average Stats by Type for Generation {generation}')
        fig.show()

    # This is the spider plot for the individual pokemon which the user entered the pokédex number of
    def show_spider_plot(self):
        try:
            # Get the pokémon's pokédex number and fetch data
            pokemon_num = int(self.pokemon_num.get())
            pokemon_data = df[df['#'] == pokemon_num]
            if pokemon_data.empty:
                messagebox.showerror("Error", f"Pokémon # {pokemon_num} not found.")
                return

            # The Pokémon stats are extracted
            stats = pokemon_data[['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']].values.flatten()
            categories = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']

            # Create Radar Chart (Spider Plot)
            fig = go.Figure()
            fig.add_trace(
                go.Scatterpolar(r=stats, theta=categories, fill='toself', name=pokemon_data['Name'].values[0])
            )
            fig.update_layout(
                polar=dict(bgcolor="#E0ACD5", radialaxis=dict(visible=True, range=[0, 150])),
                showlegend=False,
                title=f'Stats for {pokemon_data["Name"].values[0]}',
                font=dict(family="Montserrat SemiBold", size=14, color="black")
            )

            # Used to Load and display the Pokémon image in Canvas with a frame
            image_url = f"https://assets.pokemon.com/assets/cms2/img/pokedex/full/{pokemon_num:03}.png"  # The image is pulled from the official pokemon website
            response = urllib.request.urlopen(image_url)  # Sends a request to the image URL and obtains the image which is stored as raw data
            img_data = response.read()   # The raw image data is read and converted to raw binary
            img = Image.open(BytesIO(img_data))  # Creates an in-memory binary stream, Pillow interacts with the image as if it were stored in a file
            img = img.resize((250, 250))  # Size of the pokémon's image
            img = ImageTk.PhotoImage(img)   # Converts the resized image into a compatible format with the Tkinter window
            frame_width = 35  # Thickness of the golden frame

            # A new Frame for the image and stats
            if not hasattr(self, 'image_frame'):
                self.image_frame = tk.Frame(self.root, bg="#9593D9")
                self.image_frame.grid(row=7, column=0, columnspan=4, pady=10)

            # Frame is cleared and image is displayed with the frame
            for widget in self.image_frame.winfo_children():
                widget.destroy()  # Previous content is removed completely

            # Canvas for Pokémon image with a golden frame
            image_canvas = tk.Canvas(
                self.image_frame, width=250 + 2 * frame_width, height=300 + 2 * frame_width, bg="#E63462",
                highlightthickness=0
            )
            image_canvas.grid(row=0, column=0, padx=10)
            image_canvas.create_rectangle(
                0, 0, 250 + 2 * frame_width, 250 + 2 * frame_width, outline="#FFD700", width=frame_width
            )
            image_canvas.create_image(frame_width, frame_width, anchor=tk.NW, image=img)
            image_canvas.image = img  # Reference is kept to prevent garbage collection

            # Pokemon name is added below the image
            name = pokemon_data['Name'].values[0]
            image_canvas.create_text(
                125 + frame_width, 280 + frame_width + 18, text=name, font=("Montserrat SemiBold", 15, "bold"),
                fill="#FFD700"
            )

            # Pokémon stats are displayed next to the image
            stats_text = (
                f"\nNAME:  {pokemon_data['Name'].values[0]}\n"
                f"\nTYPE 1:  {pokemon_data['Type 1'].values[0]}\n"
                f"TYPE 2:  {pokemon_data['Type 2'].values[0]}\n"
                f"\nHP:  {pokemon_data['HP'].values[0]}\n"
                f"ATTACK:  {pokemon_data['Attack'].values[0]}\n"
                f"DEFENSE:  {pokemon_data['Defense'].values[0]}\n"
                f"SP. ATK:  {pokemon_data['Sp. Atk'].values[0]}\n"
                f"SP. DEF:  {pokemon_data['Sp. Def'].values[0]}\n"
                f"SPEED:  {pokemon_data['Speed'].values[0]}\n"
                f"\nTOTAL:  {pokemon_data['Total'].values[0]}\n"
            )
            stats_label = tk.Label(
                self.image_frame,
                text=stats_text,
                font=("Montserrat SemiBold", 14, "bold"),
                bg="#E63462",
                fg="#FFD700",
                justify="left",
                padx=30,  # Horizontal padding
                pady=5  # Vertical padding
            )
            stats_label.grid(row=0, column=1, padx=10, sticky="nw")

            # Shows Spider Plot
            fig.show()

        # In case the user has not enter a pokédex number and still pressed the "Show Pokemon Stats" button
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid Pokémon number.")


    # Supports the comparison of any two pokémon (pokédex number should be entered for both by the user)
    def open_comparison_page(self):
        # A new top-level window for comparison
        self.compare_window = tk.Toplevel(self.root)
        self.compare_window.title("Pokémon Comparison")
        self.compare_window.geometry("1000x800")
        self.compare_window.configure(bg="#9593D9")

        # Button Styling for this new window
        style = ttk.Style()
        style.configure("TButton", font=("Montserrat SemiBold", 12, "bold"), foreground="#291528", background="#E63462",
                        padding=10)
        style.map("TButton",
                  foreground=[("pressed", "#7C90DB"), ("active", "#E63462")],
                  background=[("pressed", "!disabled", "#ff66b2"), ("active", "#ff66b2")])

        style.configure("Custom.TLabel", font=("Montserrat SemiBold", 14), foreground="white", background="#E63462")
        button_width = 40  # The fixed width for the buttons

        # Labels and entries for Pokémon numbers
        ttk.Label(self.compare_window, text="Pokedex Number for First Pokemon:", style="Custom.TLabel").grid(row=0,
                                                                                                             column=0,
                                                                                                             padx=10,
                                                                                                             pady=10)
        self.pokemon1_num = tk.StringVar()
        self.pokemon1_entry = ttk.Entry(self.compare_window, textvariable=self.pokemon1_num, width=40)
        self.pokemon1_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.compare_window, text="Pokedex Number for Second Pokemon:", style="Custom.TLabel").grid(row=1,
                                                                                                              column=0,
                                                                                                              padx=10,
                                                                                                              pady=10)
        self.pokemon2_num = tk.StringVar()
        self.pokemon2_entry = ttk.Entry(self.compare_window, textvariable=self.pokemon2_num, width=40)
        self.pokemon2_entry.grid(row=1, column=1, padx=10, pady=10)

        # Compare button
        self.compare_stats_button = ttk.Button(self.compare_window, text="Compare Stats", command=self.compare_stats)
        self.compare_stats_button.grid(row=2, column=0, columnspan=1, pady=20)

    # Generates the spider plot with stats of both the pokemon being compared
    def compare_stats(self):
        try:
            # Gets the Pokémon numbers from user input
            pokemon1_num = int(self.pokemon1_num.get())
            pokemon2_num = int(self.pokemon2_num.get())

            # Retrieves data for both Pokémon
            pokemon1_data = df[df['#'] == pokemon1_num]
            pokemon2_data = df[df['#'] == pokemon2_num]

            # Checks if both Pokémon exist
            if pokemon1_data.empty or pokemon2_data.empty:
                messagebox.showerror("Error", "One or both Pokémon not found.")
                return

            # Extracts stats
            pokemon1_stats = pokemon1_data[['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']].values.flatten()
            pokemon2_stats = pokemon2_data[['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']].values.flatten()
            categories = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']

            # Radar Chart
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(r=pokemon1_stats, theta=categories, fill='toself',
                                          name=pokemon1_data['Name'].values[0]))
            fig.add_trace(go.Scatterpolar(r=pokemon2_stats, theta=categories, fill='toself',
                                          name=pokemon2_data['Name'].values[0]))
            fig.update_layout(
                polar=dict(bgcolor="#E0ACD5", radialaxis=dict(visible=True, range=[0, 150])),
                showlegend=True,
                title=f'Stats Comparison: {pokemon1_data["Name"].values[0]} vs {pokemon2_data["Name"].values[0]}'
            )
            fig.show()

            # Images of both Pokémon are displayed
            img1 = self.get_pokemon_image(pokemon1_num)
            img2 = self.get_pokemon_image(pokemon2_num)
            self.show_pokemon_images(img1, img2)

        except ValueError:
            messagebox.showerror("Error", "Please enter valid Pokémon numbers.")

    # Another separate function to get the pokemon image
    def get_pokemon_image(self, pokemon_num):
        image_url = f"https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/{pokemon_num:03}.png"
        response = urllib.request.urlopen(image_url)
        img_data = response.read()
        img = Image.open(BytesIO(img_data)).resize((300, 300))
        return ImageTk.PhotoImage(img)

    def show_pokemon_images(self, img1, img2):
        # Images of both Pokémon will be displayed on the comparison page
        img_label1 = tk.Label(self.compare_window, image=img1)
        img_label1.grid(row=3, column=0, pady=10)
        img_label1.image = img1  # Reference is kept

        img_label2 = tk.Label(self.compare_window, image=img2)
        img_label2.grid(row=3, column=1, pady=10)
        img_label2.image = img2  # Reference is kept

    # Bar Plot to show how many pokemon have a secondary type and how the types are distributed (generation wise)
    def show_secondary_type_distribution(self):
        try:
            # Selected Generation is fetched
            selected_generation = self.gen_var.get()

            # Data is filtered to include only Pokémon from the selected generation with a secondary type
            generation_data = df[(df['Generation'] == selected_generation) & (df['Type 2'].notna())]

            # Occurrences of each secondary type are counted
            type_counts = generation_data['Type 2'].value_counts()

            # A bar chart with Plotly is made
            fig = px.bar(
                type_counts,
                x=type_counts.index,
                y=type_counts.values,
                labels={'x': 'Secondary Type', 'y': 'Number of Pokémon'},
                title=f'Secondary Type Distribution - Generation {selected_generation}'
            )

            # Shows the Plotly figure in a new window
            fig.show()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # List of the top 10 most powerful pokemon in the selected generation
    def show_top_10_powerful_pokemon(self, *args):
        try:
            selected_generation = self.gen_var.get()  # Fetches selected generation
            generation_data = df[df['Generation'] == selected_generation]  # Filters by generation

            # Sorts by the 'Total' column in descending order and gets the top 10
            top_10_pokemon = generation_data.nlargest(10, 'Total')

            if top_10_pokemon.empty:
                messagebox.showinfo("Info", f"No Pokémon found for Generation {selected_generation}.")
                return  # Exits if no Pokémon are found

            # Creates new window
            top_10_window = tk.Toplevel(self.root)
            top_10_window.title(f"Top 10 Most Powerful Pokémon - Generation {selected_generation}")

            # Creates a frame to contain the canvas and scrollbar
            container = tk.Frame(top_10_window)
            container.pack(fill="both", expand=True)

            # Creates a canvas with a scrollbar
            canvas = tk.Canvas(container, height=500)
            scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            # Packs the canvas and scrollbar
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            # A loop is performed to display each Pokémon's stats and images in the scrollable frame
            for index, row in top_10_pokemon.iterrows():
                pokedex_number = row['#']  # Pokedex number is stored in column '#'
                name = row['Name']
                stats = (f"HP: {row['HP']}, Attack: {row['Attack']}, Defense: {row['Defense']}, "
                         f"Sp. Atk: {row['Sp. Atk']}, Sp. Def: {row['Sp. Def']}, Speed: {row['Speed']}, Total: {row['Total']}")

                # Fetches image from URL
                image_url = f"https://assets.pokemon.com/assets/cms2/img/pokedex/full/{pokedex_number:03}.png"
                response = requests.get(image_url)
                image_data = Image.open(BytesIO(response.content))
                image_data = image_data.resize((120, 120))  # Resizing
                image = ImageTk.PhotoImage(image_data)

                # Displays Pokémon's data and image in the scrollable frame
                frame = tk.Frame(scrollable_frame)
                frame.pack(pady=10, padx=10, anchor="w")

                # Image is displayed
                image_label = tk.Label(frame, image=image)
                image_label.image = image  # Keep reference to prevent garbage collection
                image_label.grid(row=0, column=0, rowspan=2, padx=10)

                # Displays Pokémon name and stats
                name_label = tk.Label(frame, text=name, font=("Arial", 14, "bold"))
                name_label.grid(row=0, column=1, sticky='w', padx=10)
                stats_label = tk.Label(frame, text=stats, font=("Arial", 10))
                stats_label.grid(row=1, column=1, sticky='w', padx=10)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # List of the Legendary Pokemon of the selected generation
    def show_legendary_pokemon_window(self, *args):
        try:
            selected_generation = self.gen_var.get()  # Fetches the selected generation
            generation_data = df[df['Generation'] == selected_generation]  # Filters by generation

            # Filter is adjusted for boolean True if the column is not a string
            legendary_pokemon = generation_data[generation_data['Legendary'] == True]

            if legendary_pokemon.empty:
                messagebox.showinfo("Info", f"No legendary Pokémon found for Generation {selected_generation}.")
                return  # Exits if no legendary Pokémon are found

            # New window is created
            legendary_window = tk.Toplevel(self.root)
            legendary_window.title(f"Legendary Pokémon - Generation {selected_generation}")

            # Creates a frame to contain the canvas and scrollbar
            container = tk.Frame(legendary_window)
            container.pack(fill="both", expand=True)

            # Creates a canvas with a scrollbar
            canvas = tk.Canvas(container, height=500)
            scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            # Packs the canvas and scrollbar
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            # A loop is performed to display each legendary Pokémon's stats and image in the scrollable frame
            for index, row in legendary_pokemon.iterrows():
                pokedex_number = row['#']  # Pokedex number is stored in column '#'
                name = row['Name']
                stats = (f"HP: {row['HP']}, Attack: {row['Attack']}, Defense: {row['Defense']}, "
                         f"Sp. Atk: {row['Sp. Atk']}, Sp. Def: {row['Sp. Def']}, Speed: {row['Speed']}")

                # Fetches image from URL
                image_url = f"https://assets.pokemon.com/assets/cms2/img/pokedex/full/{pokedex_number:03}.png"
                response = requests.get(image_url)
                image_data = Image.open(BytesIO(response.content))
                image_data = image_data.resize((120, 120))  # Resize for display
                image = ImageTk.PhotoImage(image_data)

                # Displays Pokémon data and image in a scrollable frame
                frame = tk.Frame(scrollable_frame)
                frame.pack(pady=10, padx=10, anchor="w")

                # Displays image
                image_label = tk.Label(frame, image=image)
                image_label.image = image  # Reference is kept to prevent garbage collection
                image_label.grid(row=0, column=0, rowspan=2, padx=10)

                # Displays Pokémon name and stats
                name_label = tk.Label(frame, text=name, font=("Arial", 14, "bold"))
                name_label.grid(row=0, column=1, sticky='w', padx=10)
                stats_label = tk.Label(frame, text=stats, font=("Arial", 10))
                stats_label.grid(row=1, column=1, sticky='w', padx=10)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Pokemon having the highest of each state
    def show_best_pokemon_for_each_stat(self):
        # Selected generation
        generation = self.gen_var.get()

        # Filters the DataFrame for the selected generation
        filtered_df = df[df['Generation'] == generation]

        # Identifies the Pokémon with the highest value for each stat
        stats_to_check = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']
        best_pokemon = {}

        for stat in stats_to_check:
            max_stat_row = filtered_df.loc[filtered_df[stat].idxmax()]
            best_pokemon[stat] = max_stat_row

        # Results will be displayed on a new window
        self.best_pokemon_window = tk.Toplevel(self.root)
        self.best_pokemon_window.title(f"Top Pokémon for Each Stat - Generation {generation}")
        self.best_pokemon_window.geometry("1200x400")
        self.best_pokemon_window.configure(bg="#9593D9")

        stat_label_title = ttk.Label(self.best_pokemon_window,
                                     text=f"Best Pokemon for Each Stat in Generation {generation}",
                                     style="Custom.TLabel")
        stat_label_title.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        row_num = 1
        for stat, pokemon_data in best_pokemon.items():
            # Displays stat name
            stat_label = ttk.Label(self.best_pokemon_window, text=f"Highest {stat}:", style="Custom.TLabel")
            stat_label.grid(row=row_num, column=0, padx=10, pady=5, sticky="w")

            # Pokémon name and stats are displayed
            pokemon_name = pokemon_data['Name']
            pokemon_stats = ", ".join([f"{col}: {pokemon_data[col]}" for col in stats_to_check])
            pokemon_label = ttk.Label(self.best_pokemon_window, text=f"{pokemon_name} - {pokemon_stats}",
                                      style="Custom.TLabel")
            pokemon_label.grid(row=row_num, column=1, padx=10, pady=5, sticky="w")

            row_num += 1

    def open_prediction_window(self):
        prediction_window = tk.Toplevel(self.root)   # Another window opens
        prediction_window.title("Team Prediction")   # Name of the new window
        prediction_window.configure(bg="#9593D9")    # Background color of the new window

        # Labels and input fields for Team 1
        tk.Label(prediction_window, text="Enter Pokedex Numbers for Team 1:").grid(row=0, column=0, columnspan=6, pady=10)
        team1_entries = [tk.Entry(prediction_window, width=10) for _ in range(6)]
        for i, entry in enumerate(team1_entries):
            entry.grid(row=1, column=i, padx=5, pady=5)

        # Placeholders for Pokémon images for Team 1
        team1_image_labels = [tk.Label(prediction_window, text="") for _ in range(6)]
        for i, label in enumerate(team1_image_labels):
            label.grid(row=2, column=i, padx=5, pady=5)

        # Labels and input fields for Team 2
        tk.Label(prediction_window, text="Enter Pokedex Numbers for Team 2:").grid(row=3, column=0, columnspan=6, pady=10)
        team2_entries = [tk.Entry(prediction_window, width=10) for _ in range(6)]
        for i, entry in enumerate(team2_entries):
            entry.grid(row=4, column=i, padx=5, pady=5)

        # Placeholders for Pokémon images for Team 2
        team2_image_labels = [tk.Label(prediction_window, text="") for _ in range(6)]
        for i, label in enumerate(team2_image_labels):
            label.grid(row=5, column=i, padx=5, pady=5)

        # Button to trigger prediction and update images
        predict_button = ttk.Button(
            prediction_window,
            text="Predict Winner",
            command=lambda: self.predict_and_update_images(
                team1_entries, team2_entries, team1_image_labels, team2_image_labels, prediction_window
            )
        )
        predict_button.grid(row=6, column=0, columnspan=6, pady=10)

    def calculate_team_stats(self, pokedex_numbers):
        team_stats = []

        for pokedex_number in pokedex_numbers:
            # Filters Pokémon data by Pokedex number
            pokemon_data = df[df['#'] == pokedex_number]

            if not pokemon_data.empty:
                # Extracts stats and ensure they're numeric
                stats = pokemon_data[['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']].values.flatten()  # 12 arrays will be generated at the end. Each array will have the stats of all 12 pokemon.
                stats = pd.to_numeric(stats, errors='coerce')  # Convert to numeric, setting invalid values to NaN

                # Checks if we have 6 stats and they are all numbers
                if stats.shape == (6,) and not np.isnan(stats).any():
                    team_stats.append(stats)  # An array of 6 arrays. Each interior array contains the stats of a pokemon.

        # If no valid stats are found, it returns zeros
        if len(team_stats) == 0:
            return np.zeros(6)

        # Calculate the average of the stats for the team
        team_avg_stats = np.mean(team_stats, axis=0)  # The average of each stat is found. Example: The average of all the HP's, average of all the Attack.... it returns a single array with 6 elements. Each element is a stat.
        print("Averaging of each stat: ",team_avg_stats)
        return team_avg_stats

    def predict_and_update_images(self, team1_entries, team2_entries, team1_image_labels, team2_image_labels, window):
        try:
            # Retrieves Pokedex numbers
            team1_pokedex = [int(entry.get()) for entry in team1_entries if entry.get().isdigit()]
            team2_pokedex = [int(entry.get()) for entry in team2_entries if entry.get().isdigit()]

            # Updates Pokémon images
            self.update_pokemon_images(team1_pokedex, team1_image_labels)
            self.update_pokemon_images(team2_pokedex, team2_image_labels)

            # Fetches and finds the average of stats for each team
            team1_stats = self.calculate_team_stats(team1_pokedex)          # An array which contains 6 values. Average of each stat of Team 1 is returned
            team2_stats = self.calculate_team_stats(team2_pokedex)          # An array which contains 6 values. Average of each stat of Team 2 is returned

            # Calculates the type advantages
            team1_type_advantage = self.calculate_team_type_advantage(team1_pokedex, team2_pokedex)  # A single value which is the average of all type advantages of Team 1 is returned
            team2_type_advantage = self.calculate_team_type_advantage(team2_pokedex, team1_pokedex)  # A single value which is the average of all type advantages of Team 2 is returned

            # Loads the updated model
            model = joblib.load("pokemon_model_with_type.pkl")

            # Predicts team strength using averaged stats and type advantage
            team1_score = model.predict([np.append(team1_stats, team1_type_advantage)])[0]    # Model predicts with average stats array and average type advantage value
            team2_score = model.predict([np.append(team2_stats, team2_type_advantage)])[0]    # Model predicts with average stats array and average type advantage value
            # The model.predict() function expects a 2D array as input, where each row corresponds to one "observation". In this case, a team with its stats and type advantage.
            # Since it's a regression model, the model's learned coefficients and weights are used to compute a prediction value.

            # Calculates win percentages
            total_score = team1_score + team2_score
            team1_win_rate = (team1_score / total_score) * 100
            team2_win_rate = (team2_score / total_score) * 100

            # Displays the prediction result with win rates
            result = f"Team 1 Win Rate: {team1_win_rate:.2f}%\nTeam 2 Win Rate: {team2_win_rate:.2f}%"
            messagebox.showinfo("Prediction Result", result)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


    def calculate_team_type_advantage(self, team_pokedex, opponent_pokedex): # This function calculates the type advantage of each pokemon in Team 1 with every pokemon of team 2. This means there will be a total of 36 comparisons
        type_advantages = []
        for pokedex_number in team_pokedex: # Iterates through the pokemon in team 1
            pokemon = df[df['#'] == pokedex_number].iloc[0]  # Selects the specific row in the dataframe
            for opponent_number in opponent_pokedex:  # Iterates through the pokemon in team 2
                opponent = df[df['#'] == opponent_number].iloc[0]  # Selects the specific row in the dataframe
                advantage = calculate_type_advantage(pokemon['Type 1'], pokemon['Type 2'], opponent['Type 1'], opponent['Type 2']) # Calculates type advantage for each pokemon
                type_advantages.append(advantage)  # Contains 36 values. Combination of all comparisons

        return np.mean(type_advantages) # Mean of all the 36 values is returned

    def update_pokemon_images(self, pokedex_numbers, image_labels):
        image_base_url = "https://assets.pokemon.com/assets/cms2/img/pokedex/full/{:03}.png"

        for i, pokedex_number in enumerate(pokedex_numbers):
            try:
                # Fetches Pokémon image
                image_url = image_base_url.format(pokedex_number)
                image = Image.open(requests.get(image_url, stream=True).raw).resize((200, 200))  # Resize for uniformity
                photo = ImageTk.PhotoImage(image)

                # Updates the label with the image
                image_labels[i].config(image=photo)
                image_labels[i].image = photo  # Keep a reference to avoid garbage collection
            except Exception:
                # If an error occurs (e.g., invalid Pokedex number), it shows "N/A"
                image_labels[i].config(text="N/A", image="")



# Driver Code
root = tk.Tk()  # creating the main application window using Tkinter
app = PokemonDashboard(root)  # Instance of PokemonDashboard that takes Tkinter window as argument
root.mainloop() # keeps the program alive until the user manually closes the application window (or else it will open and close immediately)
