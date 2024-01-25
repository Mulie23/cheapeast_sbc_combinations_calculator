import tkinter as tk  # Import the tkinter library for GUI
from itertools import combinations_with_replacement  # Import a function for generating combinations
import webbrowser  # Import webbrowser module to open a webpage
import json  # Import JSON module for handling data in JSON format
import os  # Import the os module for interacting with the operating system
from tkinter import messagebox  # Import the messagebox module for displaying alerts
import pyperclip  # Import the pyperclip module for copying text to the clipboard

# Define player_prices as a global variable to store player prices
player_prices = {}

# Define a function to save price data to a JSON file
def save_price_data(price_data):
    with open('price_data.json', 'w') as f:
        json.dump(price_data, f)

# Define a function to load price data from a JSON file
def load_price_data():
    if os.path.exists('price_data.json'):
        with open('price_data.json', 'r') as f:
            return json.load(f)
    else:
        return None  # or return a default price

# Define a function to open a specific webpage
def open_webpage():
    webbrowser.open('https://www.futbin.com/stc/cheapest')

# Define a function to generate team combinations based on player ratings and target rating
def generate_team_combinations(players, target_rating):
    # Check if the first player is an empty string and handle accordingly
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
        team_sum = sum(players) + sum(combo)
        average_rating = team_sum / 11
        ext_sum = 0.0
        for i in combo:
            if i > average_rating:
                ext_sum += (i - average_rating)
        for j in players:
            if j > average_rating:
                ext_sum += (j - average_rating)
        final_sum = team_sum + ext_sum
        final_rating = final_sum/11
        if final_rating - target_rating > -0.042:
            valid_combinations.append(list(combo))
    return valid_combinations

# Define a function to calculate the total price of a combination
def calculate_combination_price(combination, prices):
    return sum(prices[str(int(rating))] for rating in combination)

# Define a function to get the top N cheapest combinations
def get_top_n_cheapest_combinations(all_combinations, prices, top_n=7):
    combinations_with_prices = [(combination, calculate_combination_price(combination, prices)) for combination in all_combinations]
    sorted_combinations = sorted(combinations_with_prices, key=lambda x: x[1])
    return sorted_combinations[:top_n]

# Define a function to update player prices and display an alert
def update_player_prices():
    # Get player prices from entry fields
    for rating in range(79, 93):
        price_entry = price_entries[rating - 79]
        try:
            price = int(price_entry.get())
        except ValueError:
            price = 0  # Set a default price if the entry is not a valid integer
        player_prices[rating] = price

    save_price_data(player_prices)

    # Update entry fields with the latest prices
    for rating in range(79, 93):
        price_entries[rating - 79].delete(0, tk.END)
        price_entries[rating - 79].insert(0, player_prices.get(rating, ""))
    show_alert()

# Define a function to handle the "Calculate" button click event
def on_calculate_button_click():
    result_text.delete("1.0","end")
    input_players = entry_players.get()
    input_target_rating = int(entry_target_rating.get())

    # Convert input string to a list of player ratings
    players_list = input_players.split(",")

    # Generate all possible team compositions within the tolerance
    result = generate_team_combinations(players_list, input_target_rating)

    # Get the top 7 cheapest combinations
    top_combinations = get_top_n_cheapest_combinations(result, player_prices)

    # Display the results in the result_text
    result_text.insert(tk.END,"最便宜的七种方案：")
    for combination, total_price in top_combinations:
        result_text.insert(tk.END,f"\n方案：{combination}，总价：{total_price}")
    messagebox.showinfo("方案计算完毕", "方案计算完毕")

# Define a function to display an alert about price changes
def show_alert():
    messagebox.showinfo("价格改动", "价格已重新设置")

# Define a function to copy the result to the clipboard
def copy_result_to_clipboard():
    result = result_text.get("1.0", "end-1c")  # Get the text from the result_text widget
    pyperclip.copy(result)  # Copy the result to the clipboard
    messagebox.showinfo("方案已复制", "方案已复制到剪贴板")

# Function to remove the last player from the entry field
def remove_last_player():
    current_text = entry_players.get()
    if current_text:
        # Split the text by commas, remove the last element, and join the rest back together
        players = current_text.split(",")
        players.pop()
        new_text = ",".join(players)
        # Clear the entry and insert the new text
        entry_players.delete(0, tk.END)
        entry_players.insert(tk.END, new_text)

# Function to clear the entry field
def clear_entry():
    entry_players.delete(0, tk.END)

# Function to add a number to the entry field
def add_number_to_entry(number):
    current_text = entry_players.get()
    if current_text:
        # Add a comma and the number if the entry is not empty
        entry_players.insert(tk.END, f",{number}")
    else:
        # Add the number without a comma if the entry is empty
        entry_players.insert(tk.END, str(number))

# Tkinter GUI setup
root = tk.Tk()
root.title("实时最便宜SBC方案计算器（牧列自制）v3")
root.geometry("650x520")

# Input labels and entry widgets
label_players = tk.Label(root, text="输入球员评分（逗号分隔不同球员）：")
entry_players = tk.Entry(root,width=32)

label_target_rating = tk.Label(root, text="输入预期总评：")
entry_target_rating = tk.Entry(root,width=17)

# Input labels and entry widgets for rating prices
label_prices = tk.Label(root, text="输入实时价格：")

# Entry fields for individual player prices
price_entries = []
for rating in range(79, 93):
    label_price = tk.Label(root, text=f"评分 {rating}：")
    entry_price = tk.Entry(root)
    price_entries.append(entry_price)

    label_price.place(x=10 + (rating - 79) % 3 * 210, y=140 + (rating - 79) // 3 * 40, anchor="w")
    entry_price.place(x=80 + (rating - 79) % 3 * 210, y=140 + (rating - 79) // 3 * 40, anchor="w")

# Default player prices (replace these with your actual prices)
if os.path.exists('price_data.json'):
    with open('price_data.json', 'r') as f:
        player_prices = json.load(f)
else:
    player_prices = {"79": 400, "80": 450, "81": 700, "82": 750, "83": 900, "84": 1700, "85": 4000, "86": 7800, "87": 14250, "88": 20500, "89": 36500, "90": 55000, "91": 73000, "92": 109000}

# Set default values for entry fields
entry_players.insert(0, "")  # 示例默认球员评分
entry_target_rating.insert(0, "83")  # 示例默认目标球队评分
for rating in range(79, 93):
    price_entries[rating - 79].insert(0, player_prices.get(str(rating)))  # 默认价格

# Buttons to calculate combinations and set prices
calculate_button = tk.Button(root, text="查询方案", command=on_calculate_button_click,width=17)
set_prices_button = tk.Button(root, text="设置实时价格", command=update_player_prices,width=15)

# Label to display results
result_text = tk.Text(root,width=87,height=9)
result_text.insert(tk.END,"点击查询方案后将在这里显示结果")

# Create buttons for each rating and place them in the GUI
for rating in range(79, 93):
    button = tk.Button(root, text=str(rating), command=lambda rating=rating: add_number_to_entry(rating),width=5)
    if rating <= 85:
        # Place the buttons with ratings from 79 to 85 in the first row
        button.place(x=10 + (rating - 79) * 70, y=50, anchor="w")
    else:
        # Place the buttons with ratings from 86 to 92 in the second row
        button.place(x=10 + (rating - 86) * 70, y=80, anchor="w")

# Create a button that removes the last player from the entry_players field when clicked
remove_last_player_button = tk.Button(root, text="移除最后一位球员", command=remove_last_player,width=15)

# Create a button that clears the entry_players field when clicked
clear_button = tk.Button(root, text="归零", command=clear_entry,width=15)

# Create a button that opens the FUTBIN website to check real-time prices when clicked
futbin_price_button = tk.Button(root, text="打开FUTBIN查看实时价格", command=open_webpage)

# Create a button that copies the solution to the clipboard when clicked
copy_result_button = tk.Button(root, text="一键复制方案", command=copy_result_to_clipboard,width=17)

# Create a label with the text "牧列自制v3"
name_label = tk.Label(root, text="牧列自制v3")

# Place layout
label_players.place(x=10, y=10, anchor="w")
entry_players.place(x=230, y=10, anchor="w")

label_target_rating.place(x=435, y=10, anchor="w")
entry_target_rating.place(x=520, y=10, anchor="w")

clear_button.place(x=510, y=80, anchor="w")
remove_last_player_button.place(x=510, y=50, anchor="w")

label_prices.place(x=10, y=110, anchor="w")

calculate_button.place(x=10, y=320)
set_prices_button.place(x=250, y=320)
futbin_price_button.place(x=450, y=320)

result_text.place(x=10, y=420, anchor="w")

copy_result_button.place(x=10, y=500,anchor="w")
name_label.place(x=540, y=500, anchor="w")

# Run the Tkinter event loop
root.mainloop()
