
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import joblib

# Loads Pokémon data
df = pd.read_excel("pokemon_updated.xlsx")

# type matchup matrix
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

def calculate_type_advantage(pokemon_type1, pokemon_type2, opponent_type1, opponent_type2):  # The type advantage a pokemon has over the other
    score = 1.0  # Begins with neutral effectiveness

    # Primary type advantage (The primary type of the pokemon is compared with both primary and secondary type of opponent)
    if pokemon_type1 in type_matchup and opponent_type1 in type_matchup[pokemon_type1]:
        score *= type_matchup[pokemon_type1][opponent_type1]   # Score is multiplied by the effectiveness value in the matrix
    if pokemon_type1 in type_matchup and opponent_type2 in type_matchup[pokemon_type1]:
        score *= type_matchup[pokemon_type1][opponent_type2]   # Score is multiplied by the effectiveness value in the matrix (This is for the second type of the opponent)

    # Secondary type advantage (if any) (The secondary type of the pokemon is compared with both primary and secondary type of opponent)
    if pokemon_type2 and pokemon_type2 in type_matchup:
        if opponent_type1 in type_matchup[pokemon_type2]:
            score *= type_matchup[pokemon_type2][opponent_type1]
        if opponent_type2 in type_matchup[pokemon_type2]:
            score *= type_matchup[pokemon_type2][opponent_type2]

    return score  # Returns the overall type effectiveness of the pokemon against the opponent

def calculate_average_type_advantage(row, df):  # Computes the average type advantage of a Pokémon (row) against all other Pokémon in the DataFrame (df)
    advantages = []   # An empty list to store type advantage scores against all opponents.
    for _, opponent in df.iterrows():
        score = calculate_type_advantage(row['Type 1'], row['Type 2'], opponent['Type 1'], opponent['Type 2'])
        advantages.append(score)
    return np.mean(advantages)

# Calculates and adds 'Average Type Advantage' for each Pokémon
df['Average Type Advantage'] = df.apply(lambda row: calculate_average_type_advantage(row, df), axis=1)  # new column is added to the df Dataframe

# Preparing training data with the new feature
X = df[['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Average Type Advantage']].values  # Includes all stats of the pokemon including the type advantage
y = df['Total'].values  # The target for the regression will be the total of all the base stats and the additional 'Average Type Advantage'

# Training the model with new data
model = LinearRegression()   # Initializes a linear regression model
model.fit(X, y)   # The relationship between the features and total stats is learned
joblib.dump(model, "pokemon_model_with_type.pkl")   # Trained model is saved to a pkl file, converted into byte stream and stored on disk so it can be loaded back into memory easily
print("Model training complete with type advantages. Saved as 'pokemon_model_with_type.pkl'.")
