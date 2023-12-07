import matplotlib.pyplot as plt
import numpy as np
import time
import csv

# Function to generate random data
def generate_medals_data(countries, years):
    return np.random.randint(0, 100, size=(len(countries), len(years)))

# Function to plot chart
def plot_chart(data, countries, years, chart_type):
    plt.figure()
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
    plt.show(block=False)

# Function to record data to a CSV file
def record_data_to_csv(trial_number, data, countries, years, chart_type, filename="experiment_data.csv"):
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        if trial_number == 0:  # Write header only for the first trial
            header = ['Trial Number', 'Chart Type'] + [f'{country}_{year}' for country in countries for year in years]
            writer.writerow(header)
        
        for country_index, country in enumerate(countries):
            row = [trial_number, chart_type] + [data[country_index][year_index] for year_index in range(len(years))]
            writer.writerow(row)

# Main function
def main():
    countries = ["Country A", "Country B", "Country C", "Country D"]
    years = np.arange(2000, 2021, 4)  # Olympic years from 2000 to 2020
    num_trials = 10

    for trial in range(num_trials):
        # Generate random medals data for each trial

        medals_data = generate_medals_data(countries, years)

        # Plot area chart
        plot_chart(medals_data, countries, years, "area")
        plt.pause(1)  # Wait for 1 second
        plt.close()  # Close the area chart

        # Record data for area chart
        record_data_to_csv(trial, medals_data, countries, years, "area")

    for trial in range(num_trials):
        # Generate new random data for line chart
        new_medals_data = generate_medals_data(countries, years)
        plot_chart(new_medals_data, countries, years, "line")
        # time.sleep(1)  # Wait for 1 second
        plt.pause(1)
        plt.close() 

        # Record data for line chart
        record_data_to_csv(trial, new_medals_data, countries, years, "line")

if __name__ == "__main__":
    main()
