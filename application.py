import os
import matplotlib.pyplot as plt
import numpy as np
import csv
import time

from tkinter import *
from tkinter import Tk, Button, Label, StringVar, Radiobutton, ttk
from ttkthemes import ThemedTk

# Declare 'root' as a global variable
root = ThemedTk(theme="Breeze")

# Declare 'current_fig' as a global variable to keep track of the current figure
current_fig = None
start_time = None  # Initialize start_time
elapsed_time = 0  # Initialize elapsed_time

current_experiment_filename = None

question_list= [
    'Which country had the highest number of medals in year 2012',
    'Which country had the highest number of medals in year 2012',
    'Which country had the lowest number of medals in year 2012?',
    'Which country had the lowest number of medals in year 2012?',
    'Which country had the highest overall number of medals?',
    'Which country had the highest overall number of medals?',
    'How much difference in medals are there between the best and worst country in the year 2012',
    'How much difference in medals are there between the best and worst country in the year 2012',
    'How many medals did China win in 2000?',
    'How many medals did China win in 2000?',
    'Which country had the least number of medals in 2004?',
    'Which country had the least number of medals in 2004?',
    'Which year did the USA have its lowest medal count?',
    'Which year did the USA have its lowest medal count?',
    'How many countries had above 50 medals in 2020?',
    'How many countries had above 50 medals in 2020?',
    'what is the total number of medals won by Russia in 2004 and 2008 combined?',
    'what is the total number of medals won by Russia in 2004 and 2008 combined?',
    'How many countries had below 50 medals in 2002?',
    'How many countries had below 50 medals in 2002?',
]

#  2000 - 2020 , ["USA", "China", "UK", "Russia"]
multiple_choice_list = [
    ["USA", "China", "UK", "Russia", "All", "None"], 
    ["USA", "China", "UK", "Russia", "All", "None"],
    ["USA", "China", "UK", "Russia", "All", "None"],
    ["USA", "China", "UK", "Russia", "All", "None"],
    ["USA", "China", "UK", "Russia", "All", "None"],
    ["USA", "China", "UK", "Russia", "All", "None"],
    [1, 2, 3, 4, 5, 6], 
    [1, 2, 3, 4, 5, 6], 
    [10, 22, 50, 12, 6], 
    [10, 22, 50, 12, 6], 
    ["USA", "China", "UK", "Russia", "All", "None"], 
    ["USA", "China", "UK", "Russia", "All", "None"], 
    [2000, 2004, 2008, 2012, 2016, 2020], 
    [2000, 2004, 2008, 2012, 2016, 2020], 
    [1, 2, 3, 4, 5, 6], 
    [1, 2, 3, 4, 5, 6], 
    [30, 90, 45, 2, 5], 
    [30, 90, 45, 2, 5], 
    ["USA", "China", "UK", "Russia", "All", "None"], 
    ["USA", "China", "UK", "Russia", "All", "None"], 
]
# Function to generate random data
def generate_medals_data(countries, years):
    return np.random.randint(0, 100, size=(len(countries), len(years)))

# Function to plot chart
def plot_chart(data, countries, years, chart_type):
    global current_fig
    current_fig = plt.figure()
    if chart_type == "area":
        plt.stackplot(years, data, labels=countries, alpha=0.5)
        plt.title("Olympic Medals by Country (Area Chart)")
    elif chart_type == "line":
        for i, country in enumerate(countries):
            plt.plot(years, data[i], label=country)
            plt.fill_between(years, data[i], alpha=0.1)
        plt.title("Olympic Medals by Country (Line Chart)")
    
    plt.legend(loc='upper left')
    plt.xlabel("Year")
    plt.ylabel("Number of Medals")
    plt.xticks(years)
    plt.show(block = False)

# Callback function for the 'Next' button
def next_chart():
    global current_chart, trial, num_trials, chart_label, user_choice, medals_data, question_label, elapsed_label, timer_label, options  # Add 'root' to the global variables
    global start_time, elapsed_time  # Update global variables

    # Close the current chart if there is one
    if current_fig:
        plt.close(current_fig)

    # Record start time only at the beginning of the trial
    if trial == 0:
        start_time = time.time()

    # Update elapsed time
    elapsed_time = time.time() - start_time - 1  # Subtract 1 seconds for the delay
    elapsed_label.config(text=f"You took {round(elapsed_time, 2)} seconds to answer the question!")

    # Check user's answer
    user_answer = user_choice.get()
    if trial == 1 or trial == 2:
        correct_answer = find_highest_medals_country(medals_data, countries, years)
    elif trial == 3 or trial == 4:
        correct_answer = find_lowest_medals_country(medals_data, countries, years)
    elif trial == 5 or trial == 6:
        correct_answer = find_overall_medals_country(medals_data, countries, years)
    elif trial == 7 or trial == 8:
        correct_answer = find_different_medals_country(medals_data, countries, years)
    elif trial == 9 or trial == 10:
        correct_answer = find_china_medals_2000(medals_data, countries, years)
        multiple_choice_list[trial].append(correct_answer)
    elif trial == 11 or trial == 12:
        correct_answer = find_lowest_medals_country_2004(medals_data, countries, years)
    elif trial == 13 or trial == 14:
        correct_answer = find_lowest_USA_medals(medals_data, countries, years)
    elif trial == 15 or trial == 16:
        correct_answer = above_50_medals_2020(medals_data, countries, years)
    elif trial == 17 or trial == 18:
        correct_answer = medals_russia_2004_2008(medals_data, countries, years)
        multiple_choice_list[trial].append(correct_answer)
    elif trial == 19 or trial == 20:
        correct_answer = below_50_medals_2020(medals_data, countries, years)

    # Record data for the previous chart type
    if trial > 0:
        record_data_to_csv(trial, medals_data, countries, years, current_chart, user_answer, correct_answer, elapsed_time)

    for i in range(len(multiple_choice_list[trial])):
            options[i].config(text=f"{multiple_choice_list[trial][i]}", value=f"{multiple_choice_list[trial][i]}")
    # Generate random medals data for the next trial
    
    # Move to the next chart type (cycle between 'area' and 'line')
    current_chart = "line" if current_chart == "area" else "area"

    # Increment the trial counter
    trial += 1

    # Check if all trials are completed
    if trial <= num_trials:
        # Update the 'Next' button text
        next_button.config(text=f"See Next Chart", state='normal')
        
        # Update the chart label
        chart_label.config(text=f"Current Chart: {trial}")

        # Update the question label
        question_label.config(text=f"{question_list[trial-1]}")

        # Clear user's choice
        user_choice.set("")


        medals_data = generate_medals_data(countries, years)

        # Reset start time for the next trial
        start_time = time.time()

        # Schedule the 'show_next_chart' function after a 3-second delay
        root.after(1000, lambda: show_next_chart(medals_data))
    else:
        root.destroy()  # Close the Tkinter window when all trials are completed

# Function to show the next chart after a delay
def show_next_chart(prev_medals_data):
    # Plot the current chart type
    plot_chart(prev_medals_data, countries, years, current_chart)

def initialize_experiment():
    """
    Function to initialize the experiment by setting the correct filename.
    """
    global current_experiment_filename
    current_experiment_filename = get_next_filename()

def get_next_filename(base_filename="experiment_data"):
    """
    Function to generate the next filename based on existing files.
    """
    i = 1
    while True:
        filename = f"{base_filename}_{i}.csv"
        if not os.path.exists(filename):
            return filename
        i += 1

def record_data_to_csv(trial_number, data, countries, years, chart_type, user_answer, correct_answer, elapsed_time):
    global current_experiment_filename
    result = ''
    with open(current_experiment_filename, 'a', newline='') as file:
        writer = csv.writer(file)

        # Write header only for the first trial
        if trial_number == 1:
            header = ['Trial Number', 'Chart Type', 'User Answer', 'Question Answered Correctly','Result', 'Time Taken (seconds)'] + [f'{country}_{year}' for country in countries for year in years]
            writer.writerow(header)

        if user_answer == correct_answer:
            result = 'True'
        else:
            result = 'False'
        # Concatenate data for all countries into a single row
        row = [trial_number, chart_type, user_answer, correct_answer, result, elapsed_time] + [item for sublist in data for item in sublist]
        writer.writerow(row)



# Function to check if the user's answer is correct
def check_answer(user_answer, correct_chart_type):
    return user_answer.lower() == correct_chart_type.lower()

# Function to check the highest medals for each trail
def find_highest_medals_country(medals_data, countries, years):

    years_list = list(years)
    index_2012 = years_list.index(2012)
    medals_2012 = medals_data[:, index_2012]
    max_medals_index = np.argmax(medals_2012)
    return countries[max_medals_index]

def find_lowest_medals_country(medals_data, countries, years):
    years_list = list(years)
    index_2012 = years_list.index(2012)
    medals_2012 = medals_data[:, index_2012]
    min_medals_index = np.argmin(medals_2012)
    return countries[min_medals_index]

def find_overall_medals_country(medals_data, countries, years):
    total_medals_per_country = np.sum(medals_data, axis=1)
    max_medal = np.argmax(total_medals_per_country)

    return countries[max_medal]

def find_different_medals_country(medals_data, countries, years):
    years_list = list(years)
    index_2012 = years_list.index(2012)
    medals_2012 = medals_data[:, index_2012]
    max_medals_index = np.argmax(medals_2012)
    min_medals_index = np.argmin(medals_2012)
    return max_medals_index - min_medals_index

def find_china_medals_2000(medals_data, countries, years):
    countries_list = list(countries)
    china = countries_list.index("China")
    medals_china = medals_data[china , :]
    return medals_china[list(years).index(2000)]

def find_lowest_medals_country_2004(medals_data, countries, years):
    years_list = list(years)
    index_2004 = years_list.index(2004)
    medals_2004 = medals_data[:, index_2004]
    min_medals_index = np.argmin(medals_2004)
    return countries[min_medals_index]

def find_lowest_USA_medals(medals_data, countries, years):

    countries_list = list(countries)
    usa = countries_list.index("USA")
    medals_usa = medals_data[usa , :]
    min_usa_data = np.argmin(medals_usa)
    return years[min_usa_data]

def above_50_medals_2020(medals_data, countries, years):
    sum = 0
    years_list = list(years)
    index_2020 = years_list.index(2020)
    medals_2020 = medals_data[:, index_2020]
    for i in medals_2020:
        if i > 50:
            sum += 1
    return sum

def below_50_medals_2020(medals_data, countries, years):
    sum = 0
    years_list = list(years)
    index_2020 = years_list.index(2020)
    medals_2020 = medals_data[:, index_2020]
    for i in medals_2020:
        if i < 50:
            sum += 1
    return sum

def medals_russia_2004_2008(medals_data, countries, years):
    countries_list = list(countries)
    russia = countries_list.index("Russia")
    years_list = list(years)
    index_2004 = years_list.index(2004)
    index_2008 = years_list.index(2008)
    medals_2004 = medals_data[russia, index_2004]
    medals_2008 = medals_data[russia, index_2008]
    return medals_2004 + medals_2008

def main():
    global countries, years, current_chart, trial, num_trials, next_button, chart_label, user_choice, medals_data, question_label, elapsed_label, timer_label, options

    initialize_experiment()
    np.random.seed(100)

    countries = ["USA", "China", "UK", "Russia"]
    years = np.arange(2000, 2021, 4)  # Olympic years from 2000 to 2020
    num_trials = 20  # Total number of trials (5 line charts and 5 area charts)
    trial = 0  # Start from 1 since the first chart is shown immediately
    current_chart = "area"

    # Set the initial size of the Tkinter window
    root.geometry("500x300")

    # Create the 'Next' button
    next_button = ttk.Button(root, text=f"See Next Chart", command=next_chart)
    next_button.pack()

    # Create a label for the chart number
    chart_label = ttk.Label(root, text=f"Current Chart: {trial}")
    chart_label.pack()

    # Create a label for the question
    question_label = ttk.Label(root, text=f"{question_list[trial-1]}")
    question_label.pack()

    # Create radio buttons for user's choice
    user_choice = StringVar()

    options = []
    for i in multiple_choice_list[trial]:
            option = ttk.Radiobutton(root, text=f"{i}", variable=user_choice, value=f"{i}")
            options.append(option)
            option.pack()
    
    # Create a label for elapsed time
    elapsed_label = ttk.Label(root, text="")
    elapsed_label.pack()

    # Initialize medals_data for the first trial
    medals_data = generate_medals_data(countries, years)

    # Show the first chart straight away
    next_chart()

    root.mainloop()

if __name__ == "__main__":
    main()
