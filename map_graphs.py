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

    # Create a new panda frame with country name and medal data
    data_frame = pd.DataFrame({
        'Countries': first_column_values,
        'All Medals': total,
        'Gold Medals': golds,
        'Silver Medals': silver,
        'Bronze Medals': bronze
    })

    # Save the new panda frame to a new CSV file   
    data_frame.to_csv(data, index=False)

def show_graph(variable):
    map_df = gpd.read_file(fp)

    df = pd.read_csv(data, header=0)
    df = df[['Countries', variable]]

    merged = map_df.set_index('COUNTRY').join(df.set_index('Countries'))

    variable = variable

    vmin, vmax = 0, 300
    if (variable != 'All Medals'):
        vmax = 100

    fig, ax = plt.subplots(1, figsize=(10, 6))

    merged.plot(column=variable, cmap='Blues', linewidth=0.8, ax=ax, edgecolor='0.8')

    ax.axis('off')

    sm = plt.cm.ScalarMappable(cmap='Blues', norm=plt.Normalize(vmin=vmin, vmax=vmax))
    sm._A = []
    cbar = fig.colorbar(sm, ax=ax, format=FuncFormatter(lambda x, _: f'{int(x):,}'))  # Specify the format
    cbar.set_label("Amount of medals", rotation=270, labelpad=15, fontsize=14)
    cbar.ax.tick_params(labelsize=14)

    plt.show()


if __name__ == "__main__":
    random_data()
    show_graph('All Medals')
    show_graph('Gold Medals')
    show_graph('Silver Medals')
    show_graph('Bronze Medals')