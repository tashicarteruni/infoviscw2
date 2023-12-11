import matplotlib.pyplot as plt
import numpy as np
import csv

from tkinter import *
from tkinter import Tk, Button, Label, StringVar, Radiobutton, ttk
from ttkthemes import ThemedTk

# Declare 'root' as a global variable
root = ThemedTk(theme="Breeze")

# Declare 'current_fig' as a global variable to keep track of the current figure
current_fig = None

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
    plt.show()

# Callback function for the 'Next' button
def next_chart():
    global current_chart, trial, num_trials, chart_label, user_choice, medals_data, question_label, answer_label  # Add 'root' to the global variables

    # Close the current chart if there is one
    if current_fig:
        plt.close(current_fig)

    # Check user's answer
    user_answer = user_choice.get()
    correct_answer = check_answer(user_answer, current_chart)

    # Record data for the previous chart type
    if trial > 0:
        record_data_to_csv(trial, medals_data, countries, years, current_chart, user_answer, correct_answer)

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
        question_label.config(text=f"Question: What type of chart is this?")

        # Clear user's choice
        user_choice.set("")

        # Generate random medals data for the next trial
        medals_data = generate_medals_data(countries, years)

        # Schedule the 'show_next_chart' function after a 3-second delay
        root.after(3000, lambda: show_next_chart(medals_data))
    else:
        root.destroy()  # Close the Tkinter window when all trials are completed

# Function to show the next chart after a delay
def show_next_chart(prev_medals_data):
    # Plot the current chart type
    plot_chart(prev_medals_data, countries, years, current_chart)

# Function to record data to a CSV file, including user input and correctness
def record_data_to_csv(trial_number, data, countries, years, chart_type, user_answer, correct_answer, filename="experiment_data.csv"):
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        if trial_number == 1:  # Write header only for the first trial
            header = ['Trial Number', 'Chart Type', 'User Answer', 'Question Answered Correctly'] + [f'{country}_{year}' for country in countries for year in years]
            writer.writerow(header)

        # Concatenate data for all countries into a single row
        row = [trial_number, chart_type, user_answer, correct_answer] + [item for sublist in data for item in sublist]
        writer.writerow(row)

# Function to check if the user's answer is correct
def check_answer(user_answer, correct_chart_type):
    return user_answer.lower() == correct_chart_type.lower()

def main():
    global countries, years, current_chart, trial, num_trials, next_button, chart_label, user_choice, medals_data, question_label, answer_label

    countries = ["USA", "China", "UK", "Russia"]
    years = np.arange(2000, 2021, 4)  # Olympic years from 2000 to 2020
    num_trials = 10  # Total number of trials (5 line charts and 5 area charts)
    trial = 0  # Start from 1 since the first chart is shown immediately
    current_chart = "area"

    # Set the initial size of the Tkinter window
    root.geometry("400x400")

    # Create the 'Next' button
    next_button = ttk.Button(root, text=f"See Next Chart", command=next_chart)
    next_button.pack()

    # Create a label for the chart number
    chart_label = ttk.Label(root, text=f"Current Chart: {trial}")
    chart_label.pack()

    # Create a label for the question
    question_label = ttk.Label(root, text=f"Question: What type of chart is this?")
    question_label.pack()

    # Create radio buttons for user's choice
    user_choice = StringVar()
    option1 = ttk.Radiobutton(root, text="Area Chart", variable=user_choice, value="area")
    option2 = ttk.Radiobutton(root, text="Line Chart", variable=user_choice, value="line")
    option1.pack()
    option2.pack()

   # Initialize medals_data for the first trial
    medals_data = generate_medals_data(countries, years)

    # Show the first chart straight away
    next_chart()

    root.mainloop()

if __name__ == "__main__":
    main()
