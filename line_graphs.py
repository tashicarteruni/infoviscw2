import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from matplotlib.ticker import FuncFormatter

# Relative file paths
fp = "world.shp"
csv_file = 'population.csv'
data = 'data.csv'

# fucntion to generate random medal data for each country
def random_data():
    # Load the original csv file into a panda frame
    df_original = pd.read_csv(csv_file)

    # Extract the country name from the first column
    first_column_values = df_original.iloc[:, 0]
    population = df_original['Population']
    continent = df_original['Continent']

    # Generating random medals for each country
    golds = np.random.randint(0, 100, size=len(df_original))
    silver = np.random.randint(0, 100, size=len(df_original))
    bronze = np.random.randint(0, 100, size=len(df_original))
    total = golds+silver+bronze
    male = np.random.randint(0,total,size=len(df_original))
    winter_medals = np.random.randint(0, 200, size=len(df_original))
    female = total-male
    sprint = np.random.randint(0,10,size=len(df_original))
    archery = np.random.randint(0,10,size=len(df_original))
    high_jump = np.random.randint(0,10,size=len(df_original))
    swimming = np.random.randint(0,10,size=len(df_original))
    javelin = np.random.randint(0,10,size=len(df_original))
    individual_medals = np.random.randint(0, total, size=len(df_original))
    team_medals = total - individual_medals
    medals_per_capita = round(total / (population / 1_000_000))

    # Create a new panda frame with country name and medal data
    data_frame = pd.DataFrame({
        'Countries': first_column_values,
        'Continent': continent,
        'All Medals': total,
        'Winter Medals': winter_medals,
        'Gold Medals': golds,
        'Silver Medals': silver,
        'Bronze Medals': bronze,
        'Male': male,
        'Female':female,
        '100m Sprint': sprint,
        'Archery':archery,
        'High Jump':high_jump,
        '100m Swimming':swimming,
        'Javelin': javelin,
        'Individual Sports': individual_medals,
        'Team Sports': team_medals,
        'Medals per Capita': medals_per_capita
    })

    # Save the new panda frame to a new CSV file   
    data_frame.to_csv(data, index=False)

def top_countries_by_medals():
    df = pd.read_csv(data, header=0)
    top_10_countries = df.nlargest(10, 'All Medals')

    gold = '#FFD700'
    silver = '#C0C0C0'
    bronze = '#CD7F32'

    # Plotting the line graph
    plt.plot(top_10_countries['Countries'], top_10_countries['Gold Medals'], color=gold, label='Gold', marker='o')
    plt.plot(top_10_countries['Countries'], top_10_countries['Silver Medals'], color=silver, label='Silver', marker='o')
    plt.plot(top_10_countries['Countries'], top_10_countries['Bronze Medals'], color=bronze, label='Bronze', marker='o')

    plt.xlabel('Country')
    plt.ylabel('Number of Medals')
    plt.title('Top 10 Countries by Total Medals')
    plt.legend()
    plt.show()

def top_counties_by_gender():
    df = pd.read_csv(data, header=0)
    top_10_countries = df.nlargest(10, 'All Medals')

    male = "blue"
    female = "pink"

    # Plotting the line graph
    plt.plot(top_10_countries['Countries'], top_10_countries['Male'], color=male, label='Male', marker='o')
    plt.plot(top_10_countries['Countries'], top_10_countries['Female'], color=female, label='Female', marker='o')

    plt.xlabel('Country')
    plt.ylabel('Number of Medals')
    plt.title('Top 10 Countries by Total Medals for each gender')
    plt.legend()
    plt.show()

def total_medals_by_sport():
    df = pd.read_csv(data, header=0)
    top_10_countries = df.nlargest(10, 'All Medals')

    sprint = "#26547D"
    archery = "#EF436B"
    high_jump = "#FFCE5C"
    swimming = "#05C793"
    javelin = "#5C43A9"

    # Plotting the line graph
    plt.plot(top_10_countries['Countries'], top_10_countries['100m Sprint'], color=sprint, label='Sprint', marker='o')
    plt.plot(top_10_countries['Countries'], top_10_countries['Archery'], color=archery, label='Archery', marker='o')
    plt.plot(top_10_countries['Countries'], top_10_countries['High Jump'], color=high_jump, label='High Jump', marker='o')
    plt.plot(top_10_countries['Countries'], top_10_countries['100m Swimming'], color=swimming, label='Swimming', marker='o')
    plt.plot(top_10_countries['Countries'], top_10_countries['Javelin'], color=javelin, label='Javelin', marker='o')

    plt.xlabel('Country')
    plt.ylabel('Number of Medals')
    plt.title('Top 10 Countries by Total Medals for 5 sports')
    plt.legend()
    plt.show()

def compare_summer_winter():
    df = pd.read_csv(data, header=0)
    top_10_countries = df.nlargest(10, 'All Medals')

    winter = "blue"
    summer = "green"

    # Plotting the line graph
    plt.plot(top_10_countries['Countries'], top_10_countries['Winter Medals'], color=winter, label='Winter Medals', marker='o')
    plt.plot(top_10_countries['Countries'], top_10_countries['All Medals'], color=summer, label='Summer Medals', marker='o')

    plt.xlabel('Country')
    plt.ylabel('Number of Medals')
    plt.title('Top 10 Countries for Winter Medals and Summer Medals')
    plt.legend()
    plt.show()
    
def top_countries_by_individual_team():
    df = pd.read_csv(data, header=0)
    top_10_countries = df.nlargest(10, 'All Medals')

    individual = "orange"
    team = "purple"

    # Plotting the line graph
    plt.plot(top_10_countries['Countries'], top_10_countries['Individual Sports'], color=individual, label='Individual Sports', marker='o')
    plt.plot(top_10_countries['Countries'], top_10_countries['Team Sports'], color=team, label='Team Sports', marker='o')

    plt.xlabel('Country')
    plt.ylabel('Number of Medals')
    plt.title('Top 10 Countries by Medals in Individual vs. Team Sports')
    plt.legend()
    plt.show()
    
def top_countries_by_medals_per_capita():
    # Get csv into a panda frame
    df = pd.read_csv(data, header=0)

    # Sort the DataFrame by medals per capita and get the top 10 countries
    top_10_countries = df.nlargest(10, 'All Medals')

    # Plotting the line chart
    plt.plot(top_10_countries['Countries'], top_10_countries['Medals per Capita'], marker='o')

    plt.xlabel('Country')
    plt.ylabel('Medals per Capita')
    plt.title('Top 10 Countries by Medals per Capita')
    plt.show()
    
def line_chart_medals_by_continent():
    df = pd.read_csv(data, header=0)
    
    # Group by continent and sum the medals
    continent_medals = df.groupby('Continent').sum()[['All Medals']]

    # Plotting the line chart
    plt.plot(continent_medals.index, continent_medals['All Medals'], marker='o')

    plt.xlabel('Continent')
    plt.ylabel('Number of Medals')
    plt.title('Medal Counts by Continent')
    plt.show()

if __name__ == "__main__":
    random_data()
    top_countries_by_medals()
    top_counties_by_gender()
    total_medals_by_sport()
    compare_summer_winter()
    top_countries_by_individual_team()
    top_countries_by_medals_per_capita()
    line_chart_medals_by_continent()
