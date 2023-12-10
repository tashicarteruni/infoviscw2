import pandas as pd
import pycountry_convert as pc

# Function to obtain continent for a given country
def country_to_continent(country_name):
    try:
        country_alpha2 = pc.country_name_to_country_alpha2(country_name)
        country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
        country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
        return country_continent_name
    except Exception as e:
        print(f"Error processing country {country_name}: {e}")
        return None

# Read the population.csv file
population_df = pd.read_csv('population.csv')

# Apply the country_to_continent function to get continents
population_df['Continent'] = population_df['Country Name'].apply(country_to_continent)

# Display the resulting DataFrame
population_df.to_csv('population_with_continent.csv', index=False)

