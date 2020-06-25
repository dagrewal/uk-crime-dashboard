import pandas as pd
from fetch_data import fetch_data

# url where data source is located
csv_url = "https://www.ethnicity-facts-figures.service.gov.uk/crime-justice-and-the-law/policing/number-of-arrests/latest/downloads/number-of-arrests.csv"

def read_data(path_to_data):
    """
    Fetch data from url and save it to disk using fetch_data(). Reads data from disk using
    pandas library.

    Args:
        path_to_data (string) representing the location of the downloaded data.

    Returns:
        df (pandas.DataFrame) containing the downloaded dataset. 
    """

    # call fetch_data() to fetch data from the url where source is located.
    fetch_data(csv_url)

    try:
        # read downloaded data into memory
        df = pd.read_csv(path_to_data, low_memory=False)
    except Exception as e:
        print('Error reading dataset into memory!\n')
        print(e)
    return df

# call read_data()
df = read_data('../data/latest_crime_data.csv')