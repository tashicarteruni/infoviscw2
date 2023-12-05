import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from matplotlib.ticker import FuncFormatter

# Relative file paths
fp = "world.shp"
csv_file = "population.csv"

map_df = gpd.read_file(fp)

df = pd.read_csv(csv_file, header=0)
df = df[['Country', 'Refugees']]

merged = map_df.set_index('COUNTRY').join(df.set_index('Country'))

selected_countries = ['Afghanistan', 'Syria']
filtered_merged = merged.loc[selected_countries]

variable = 'Refugees'

vmin, vmax = 1000, 3500000

fig, ax = plt.subplots(1, figsize=(10, 6))

merged.plot(column=variable, cmap='Blues', linewidth=0.8, ax=ax, edgecolor='0.8')

ax.axis('off')

sm = plt.cm.ScalarMappable(cmap='Blues', norm=plt.Normalize(vmin=vmin, vmax=vmax))
sm._A = []
cbar = fig.colorbar(sm, ax=ax, format=FuncFormatter(lambda x, _: f'{int(x):,}'))  # Specify the format
cbar.set_label("Template", rotation=270, labelpad=15, fontsize=14)
cbar.ax.tick_params(labelsize=14)

plt.show()
