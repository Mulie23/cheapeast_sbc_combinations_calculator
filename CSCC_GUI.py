import tkinter as tk
from itertools import combinations_with_replacement
import webbrowser

# Define player_prices as a global variable
player_prices = {}
def open_webpage():
    webbrowser.open('https://www.futbin.com/stc/cheapest')

def generate_team_combinations(players, target_rating):
    if players[0] == '':
        players = []
    else:
        # Convert player ratings to floats
        players = [float(player) for player in players]

    # Calculate the number of players needed to reach the target team rating
    required_players = 11 - len(players)

    # Generate all combinations of player ratings to fill the remaining positions
    possible_ratings = [float(rating) for rating in range(79, 93)]  # Player ratings range from 79 to 92
    combinations = combinations_with_replacement(possible_ratings, required_players)

    # Filter combinations that are within the tolerance of the target team rating
    valid_combinations = []
    for combo in combinations:
        team_rating = (sum(players) + sum(combo)) / 11
        sub = 0
        for i in combo:
            if i > team_rating:
                sub += (i - team_rating)
        if team_rating + sub/11 - target_rating > -0.042:
            valid_combinations.append(list(combo))

    return valid_combinations

def calculate_combination_price(combination, prices):
    # Calculate the total price of a combination based on player prices
    return sum(prices[rating] for rating in combination)

def get_top_n_cheapest_combinations(all_combinations, prices, top_n=7):
    # Calculate the price for each combination
    combinations_with_prices = [(combination, calculate_combination_price(combination, prices)) for combination in all_combinations]

    # Sort combinations by price in ascending order
    sorted_combinations = sorted(combinations_with_prices, key=lambda x: x[1])

    # Return the top N cheapest combinations
    return sorted_combinations[:top_n]

def update_player_prices():
    global player_prices

    # Get player prices from entry fields
    for rating in range(79, 93):
        price_entry = price_entries[rating - 79]
        try:
            price = float(price_entry.get())
        except ValueError:
            price = 0  # Set a default price if the entry is not a valid float
        player_prices[rating] = price

    # Update entry fields with the latest prices
    for rating in range(79, 93):
        price_entries[rating - 79].delete(0, tk.END)
        price_entries[rating - 79].insert(0, player_prices.get(rating, ""))

def on_calculate_button_click():
    input_players = entry_players.get()
    input_target_rating = float(entry_target_rating.get())

    # Convert input string to list of player ratings
    players_list = input_players.split(",")

    # Set a tolerance level for the team rating
    tolerance_level = 0.1  # You can adjust this value based on your preferences

    # Update player prices based on user input
    update_player_prices()

    # Generate all possible team compositions within the tolerance
    result = generate_team_combinations(players_list, input_target_rating)

    # Get the top 7 cheapest combinations
    top_combinations = get_top_n_cheapest_combinations(result, player_prices)

    # Display the results in the result_label
    result_label.config(text="Top 7 Cheapest Combinations:")
    for combination, total_price in top_combinations:
        result_label.config(text=result_label.cget("text") + f"\nCombination: {combination}, Total Price: {total_price}")

# Tkinter GUI setup
root = tk.Tk()
root.title("Cheapest SBC Combinations Calculator")
root.geometry("620x450")

# Input labels and entry widgets
label_players = tk.Label(root, text="Enter players' ratings (comma-separated):")
entry_players = tk.Entry(root,width=28)

label_target_rating = tk.Label(root, text="Enter target team rating:")
entry_target_rating = tk.Entry(root,width=10)

# Input labels and entry widgets for rating prices
label_prices = tk.Label(root, text="Enter prices for each rating:")

# Entry fields for individual player prices
price_entries = []
for rating in range(79, 93):
    label_price = tk.Label(root, text=f"Rating {rating}:")
    entry_price = tk.Entry(root)
    price_entries.append(entry_price)

    label_price.place(x=10 + (rating - 79) % 3 * 200, y=80 + (rating - 79) // 3 * 40, anchor="w")
    entry_price.place(x=80 + (rating - 79) % 3 * 200, y=80 + (rating - 79) // 3 * 40, anchor="w")

# Default player prices (replace these with your actual prices)
default_prices = {79: 400, 80: 450, 81: 700, 82: 950, 83: 1300, 84: 2000, 85: 4500, 86: 8100, 87: 14250, 88: 20000, 89: 34500, 90: 55000, 91: 75000, 92: 107000}

# Set default values for entry fields
entry_players.insert(0, "80,82,84,86,88,90,92")  # Example default players' ratings
entry_target_rating.insert(0, "85")  # Example default target team rating
for rating in range(79, 93):
    price_entries[rating - 79].insert(0, default_prices.get(rating, ""))  # Default prices

# Buttons to calculate combinations and set prices
calculate_button = tk.Button(root, text="Calculate Combinations", command=on_calculate_button_click)
set_prices_button = tk.Button(root, text="Set Default Prices", command=update_player_prices)

# Label to display results
result_label = tk.Label(root, text="Results will be displayed here.")

# Grid layout
label_players.place(x=10, y=10, anchor="w")
entry_players.place(x=240, y=10, anchor="w")

label_target_rating.place(x=400, y=10, anchor="w")
entry_target_rating.place(x=540, y=10, anchor="w")

label_prices.place(x=10, y=50, anchor="w")

calculate_button.place(x=10, y=260)
set_prices_button.place(x=180, y=260)

result_label.place(x=10, y=350, anchor="w")

open_webpage_button = tk.Button(root, text="Futbin lowest prices", command=open_webpage)
open_webpage_button.place(x=350, y=260)

name_label = tk.Label(root, text="Coded by Mulie")
name_label.place(x=500, y=400, anchor="w")
# Run the Tkinter event loop
root.mainloop()
