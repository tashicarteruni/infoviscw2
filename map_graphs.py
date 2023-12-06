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

    # Generating random medals for each country
    golds = np.random.randint(0, 100, size=len(df_original))
    silver = np.random.randint(0, 100, size=len(df_original))
    bronze = np.random.randint(0, 100, size=len(df_original))
    total = golds+silver+bronze
    male = np.random.randint(0,total,size=len(df_original))
    female = total-male

    # Create a new panda frame with country name and medal data
    data_frame = pd.DataFrame({
        'Countries': first_column_values,
        'All Medals': total,
        'Gold Medals': golds,
        'Silver Medals': silver,
        'Bronze Medals': bronze,
        'Male': male,
        'Female':female
    })

    # Save the new panda frame to a new CSV file   
    data_frame.to_csv(data, index=False)

def top_countries_by_medals():
    # Get csv into a panda frame
    df = pd.read_csv(data, header=0)

    # Sort the DataFrame by total medals and get the top 10 countries
    top_10_countries = df.nlargest(10, 'All Medals')

    # Getting colours hexcode
    gold = '#FFD700' 
    silver = '#C0C0C0'  
    bronze = '#CD7F32'

    # Plotting the area graph
    plt.stackplot(top_10_countries['Countries'], top_10_countries['Gold Medals'], top_10_countries['Silver Medals'], top_10_countries['Bronze Medals'],
                colors=[gold, silver, bronze],labels=['Gold', 'Silver', 'Bronze'], alpha=0.7)

    # set labels and title
    plt.xlabel('Country')
    plt.ylabel('Number of Medals')
    plt.title('Top 10 Countries by Total Medals')
    # SHow legend
    plt.legend()
    # Display 
    plt.show()

def top_counties_by_gender():
    # Get csv into a panda frame
    df = pd.read_csv(data, header=0)

    # Sort the DataFrame by total medals and get the top 10 countries
    top_10_countries = df.nlargest(10, 'All Medals')

    # Get colours hexcode
    male = "blue"
    female = "pink"

    # Plotting the area graph
    plt.stackplot(top_10_countries['Countries'], top_10_countries['Male'], top_10_countries['Female'], 
                colors=[male,female],labels=['male','female'], alpha=0.7)

    # set labels and title
    plt.xlabel('Country')
    plt.ylabel('Number of Medals')
    plt.title('Top 10 Countries by Total Medals for each gender')
    # Show legend
    plt.legend()
    # Display 
    plt.show()

if __name__ == "__main__":
    random_data()
    top_countries_by_medals()
    top_counties_by_gender()
    #show_graph('Gold Medals')
    #show_graph('Silver Medals')
    #show_graph('Bronze Medals')


    