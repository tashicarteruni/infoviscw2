import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from matplotlib.ticker import FuncFormatter

# Relative file paths
fp = "world.shp"
csv_file = 'population.csv'
data = 'data.csv'

def random_data():
    # Load the original csv file into a panda frame
    df_original = pd.read_csv(csv_file)

    # Extract the country name from the first column
    first_column_values = df_original.iloc[:, 0]

    # Generating random medals for each country
    golds = np.random.randint(0, 100, size=len(df_original))
    silver = np.random.randint(0, 100, size=len(df_original))
    bronze = np.random.randint(0, 100, size=len(df_original))

    # Create a new panda frame with country name and medal data
    data_frame = pd.DataFrame({
        'Countries': first_column_values,
        'Gold Medals': golds,
        'Silver Medals': silver,
        'Bronze Medals': bronze
    })

    # Save the new panda frame to a new CSV file   
    data_frame.to_csv(data, index=False)