import matplotlib.pyplot as plt
import numpy as np
import csv
from tkinter import Tk, Button, Label, Entry

# Declare 'root' as a global variable
root = Tk()

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
    global current_chart, trial, num_trials, chart_label, user_input_entry  # Add 'root' to the global variables

    # Close the current chart if there is one
    if current_fig:
        plt.close(current_fig)

    # Generate random medals data for each trial
    medals_data = generate_medals_data(countries, years)

    # Record data for the current chart type
    record_data_to_csv(trial, medals_data, countries, years, current_chart)

    # Move to the next chart type (cycle between 'area' and 'line')
    current_chart = "line" if current_chart == "area" else "area"

    # Increment the trial counter
    trial += 1

    # Check if all trials are completed
    if trial <= num_trials:
        # Update the 'Next' button text
        next_button.config(text=f"See Next Chart ({current_chart.capitalize()})", state='normal')
        
        # Update the chart label
        chart_label.config(text=f"Current Chart: {trial}")

        # Clear the user input field
        user_input_entry.delete(0, 'end')

        # Schedule the 'show_next_chart' function after a 5-second delay
        root.after(1000, lambda: show_next_chart(medals_data))
    else:
        root.destroy()  # Close the Tkinter window when all trials are completed

# Function to show the next chart after a delay
def show_next_chart(prev_medals_data):
    # Plot the current chart type
    plot_chart(prev_medals_data, countries, years, current_chart)

# Function to record data to a CSV file, including user input
def record_data_to_csv(trial_number, data, countries, years, chart_type, filename="experiment_data.csv"):
    user_input = user_input_entry.get()  # Get user input from the Entry widget
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        if trial_number == 0:  # Write header only for the first trial
            header = ['Trial Number', 'Chart Type', 'User Input'] + [f'{country}_{year}' for country in countries for year in years]
            writer.writerow(header)
        
        for country_index, country in enumerate(countries):
            row = [trial_number, chart_type, user_input] + [data[country_index][year_index] for year_index in range(len(years))]
            writer.writerow(row)

def main():
    global countries, years, current_chart, trial, num_trials, next_button, chart_label, user_input_entry

    countries = ["USA", "China", "UK", "Russia"]
    years = np.arange(2000, 2021, 4)  # Olympic years from 2000 to 2020
    num_trials = 10  # Total number of trials (5 line charts and 5 area charts)
    trial = 0  # Start from 1 since the first chart is shown immediately
    current_chart = "area"

    # Set the initial size of the Tkinter window
    root.geometry("400x250")

    # Create the 'Next' button
    next_button = Button(root, text=f"See Next Chart ({current_chart.capitalize()})", command=next_chart)
    next_button.pack()

    # Create a label for the chart number
    chart_label = Label(root, text=f"Current Chart: {trial}")
    chart_label.pack()

    # Create an Entry widget for user input
    user_input_entry = Entry(root)
    user_input_entry.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
