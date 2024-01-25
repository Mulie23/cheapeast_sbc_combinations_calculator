import tkinter as tk
from itertools import combinations_with_replacement
import webbrowser
import json
import os
from tkinter import messagebox
import pyperclip

# Define player_prices as a global variable
player_prices = {}

# Define a function to save price data
def save_price_data(price_data):
    with open('price_data.json', 'w') as f:
        json.dump(price_data, f)

# Define a function to load price data
def load_price_data():
    if os.path.exists('price_data.json'):
        with open('price_data.json', 'r') as f:
            return json.load(f)
    else:
        return None  # or return a default price
    
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
        # if combo == (83.0,83.0,83.0,86.0,86.0,86.0,86.0,86.0):
        #     print("yes")
        team_sum = sum(players) + sum(combo)
        average_rating = team_sum / 11
        # print(team_sum)
        # print(average_rating)
        ext_sum = 0.0
        for i in combo:
            # print(i)
            if i > average_rating:
                ext_sum += (i - average_rating)
                # print(ext_sum)
        for j in players:
            # print(j)
            if j > average_rating:
                ext_sum += (j - average_rating)
                # print(ext_sum)
        final_sum = team_sum + ext_sum
        # print(final_sum)
        final_rating = final_sum/11
        # print(final_rating)
        # print(final_rating - target_rating)
        if final_rating - target_rating > -0.042:
            valid_combinations.append(list(combo))
    # print(valid_combinations[0])
    # if [83.0,84.0,84.0,85.0,85.0,85.0,85.0,85.0] in valid_combinations:
    #     print("yes")
    # else:
    #     print("no")
    return valid_combinations

def calculate_combination_price(combination, prices):
    # Calculate the total price of a combination based on player prices
    # print(combination)
    # print(prices)
    return sum(prices[str(int(rating))] for rating in combination)

def get_top_n_cheapest_combinations(all_combinations, prices, top_n=7):
    # Calculate the price for each combination
    combinations_with_prices = [(combination, calculate_combination_price(combination, prices)) for combination in all_combinations]

    # Sort combinations by price in ascending order
    sorted_combinations = sorted(combinations_with_prices, key=lambda x: x[1])

    # Return the top N cheapest combinations
    return sorted_combinations[:top_n]

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

def on_calculate_button_click():
    result_text.delete("1.0","end")
    input_players = entry_players.get()
    input_target_rating = int(entry_target_rating.get())

    # Convert input string to list of player ratings
    players_list = input_players.split(",")

    # Generate all possible team compositions within the tolerance
    result = generate_team_combinations(players_list, input_target_rating)

    # Get the top 7 cheapest combinations
    top_combinations = get_top_n_cheapest_combinations(result, player_prices)

    # Display the results in the result_text
    result_text.insert(tk.END,"最便宜的七种方案：")
    for combination, total_price in top_combinations:
        result_text.insert(tk.END,f"\n方案：{combination}，总价：{total_price}")
        # print(combination)
        # print(total_price)
    messagebox.showinfo("方案计算完毕", "方案计算完毕")

def show_alert():
    messagebox.showinfo("价格改动", "价格已重新设置")

def copy_result_to_clipboard():
    result = result_text.get("1.0", "end-1c")  # Get the text from the result_text widget
    pyperclip.copy(result)  # Copy the result to the clipboard
    messagebox.showinfo("方案已复制", "方案已复制到剪贴板")

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
# result_text = tk.Text(root, text="点击查询方案后将在这里显示结果")
result_text = tk.Text(root,width=87,height=9)
result_text.insert(tk.END,"点击查询方案后将在这里显示结果")


# Grid layout
label_players.place(x=10, y=10, anchor="w")
entry_players.place(x=230, y=10, anchor="w")

label_target_rating.place(x=435, y=10, anchor="w")
entry_target_rating.place(x=520, y=10, anchor="w")

label_prices.place(x=10, y=110, anchor="w")

calculate_button.place(x=10, y=320)
set_prices_button.place(x=250, y=320)

result_text.place(x=10, y=420, anchor="w")

open_webpage_button = tk.Button(root, text="打开FUTBIN查看实时价格", command=open_webpage)
open_webpage_button.place(x=450, y=320)

copy_result_button = tk.Button(root, text="一键复制方案", command=copy_result_to_clipboard,width=17)
copy_result_button.place(x=10, y=500,anchor="w")  # Adjust the position as needed

name_label = tk.Label(root, text="牧列自制v3")
name_label.place(x=540, y=500, anchor="w")

def add_number_to_entry(number):
    current_text = entry_players.get()
    if current_text:
        # Add a comma and the number if the entry is not empty
        entry_players.insert(tk.END, f",{number}")
    else:
        # Add the number without a comma if the entry is empty
        entry_players.insert(tk.END, str(number))

for rating in range(79, 93):
    button = tk.Button(root, text=str(rating), command=lambda rating=rating: add_number_to_entry(rating),width=5)
    if rating <= 85:
        # Place the buttons with ratings from 79 to 85 in the first row
        button.place(x=10 + (rating - 79) * 70, y=50, anchor="w")
    else:
        # Place the buttons with ratings from 86 to 92 in the second row
        button.place(x=10 + (rating - 86) * 70, y=80, anchor="w")

def clear_entry():
    entry_players.delete(0, tk.END)

clear_button = tk.Button(root, text="归零", command=clear_entry,width=15)
clear_button.place(x=510, y=80, anchor="w")  # Adjust the position as needed

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

remove_last_player_button = tk.Button(root, text="移除最后一位球员", command=remove_last_player,width=15)
remove_last_player_button.place(x=510, y=50, anchor="w")  # Adjust the position as needed

# Run the Tkinter event loop
root.mainloop()
