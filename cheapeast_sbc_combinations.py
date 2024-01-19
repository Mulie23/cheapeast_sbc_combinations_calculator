from itertools import combinations_with_replacement

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
                sub += (i-team_rating)
        if team_rating + sub/11 - target_rating>-0.042:
            valid_combinations.append(list(combo))

    return valid_combinations

# Example usage:
input_players = input("Input your players' ratings (comma-separated values): ")
input_target_rating = float(input("Input your target team rating: "))

# Convert input string to list of player ratings
players_list = input_players.split(",")

# Set a tolerance level for the team rating
tolerance_level = 0.1  # You can adjust this value based on your preferences

# Generate all possible team compositions within the tolerance
result = generate_team_combinations(players_list, input_target_rating)

# Display the results
# print("Possible team compositions with target rating:")
# for team in result:
#     print(team)



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

# Example usage:
# Assuming you have 'all_combinations' and 'player_prices' from your previous code

# Player prices dictionary (replace these with actual prices)
player_prices = {79: 400, 80: 450, 81: 700, 82: 950, 83: 1300, 84: 2000, 85: 4500, 86: 8100, 87: 14250, 88: 20000, 89: 34500, 90: 55000, 91: 75000, 92: 107000}

# Get the top 7 cheapest combinations
top_combinations = get_top_n_cheapest_combinations(result, player_prices)

# Display the results
print("Top 7 Cheapest Combinations:")
for combination, total_price in top_combinations:
    print(f"Combination: {combination}, Total Price: {total_price}")
    sub = 0
    for i in combination:
        if i > sum(combination)/11:
            sub += (i-sum(combination)/11)
    print(sum(combination)/11+sub/11)