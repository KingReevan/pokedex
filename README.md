# Pokedex Data Visualization
As a data visualization project, I've made an application that can be used to visualize pokemon statistics such as their battle stats, types, generation, overall stats etc.

A desktop application built with Python and Tkinter for visualizing Pokémon statistics by generation. This tool allows users to view various stats, filter by generation, and see specific visualizations for Legendary Pokémon, the Top 10 most powerful Pokémon, Pokémon with secondary types, and more.

Features:
1) Pokémon Statistics by Generation: Visualize Pokémon statistics for each selected generation.
2) Legendary Pokémon Viewer: A separate window showing all Legendary Pokémon from the chosen generation.
3) Top 10 Most Powerful Pokémon: Displays the top 10 Pokémon with the highest total stats from the selected generation.
4) Secondary Types Bar Chart: View a bar chart of Pokémon with secondary types in the selected generation.
5) Pokémon Stats Radar Chart: Visualize individual Pokémon stats in a radar chart format.
6) Distribution range for each stat based on generation and primary type of pokemon
7) More than fifteen different types of visualizations which offer multiple perspectives to pokemon data
   
Installation Requirements
1) Python 3.8+
2) Required packages (listed in requirements.txt)

Steps to Install
1) Clone the repository:
     git clone https://github.com/KingReevan/pokedex.git
2) Install the dependencies (In requirements.txt):
     pip install -r requirements.txt
3) Run the application:
     python main.py

If you prefer to run the application as a standalone executable, use the following command to create an .exe file:
pyinstaller --onefile --windowed --add-data "pokemon_updated.xlsx;." --icon=mankey.ico main.py

Folder Structure:

.

├── main.py                  # Main application code

├── pokemon_updated.xlsx     # Pokémon data file

├── mankey.ico               # Application icon

├── requirements.txt         # List of dependencies

└── README.md                # Project documentation


Usage:

1)Select a generation to visualize statistics.

2)Use the various buttons for different types of visualizations:
  + Legendary Pokémon: Opens a window with all Legendary Pokémon for the chosen generation.
  + Top 10 Most Powerful Pokémon: Displays a list of the most powerful Pokémon for the chosen generation.
  + Secondary Types: Shows a bar chart of Pokémon with a secondary type.
  + Radar Chart: Displays a radar chart with stats for a chosen Pokémon.

Contributions are welcome! Please open an issue or submit a pull request.
