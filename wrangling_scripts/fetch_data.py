import requests
import io
from os import path
import gc
import pandas as pd

def fetch_data(path_to_data, file_name='../data/latest_crime_data.csv'):
    """
    Request the dataset from 
    https://www.ethnicity-facts-figures.service.gov.uk/crime-justice-and-the-law/policing/number-of-arrests/.

    Args:
        path_to_data (string) representing the url of the data (csv).
        file_name (string) representing the location to store the downloaded data.

    Returns:
        ../data/latest_crime_data.csv containing the raw data from the url.
        The size of the new file and whether or not it has been overwritten or newly created.
    """
    no_content_error_message = 'No content has been downloaded! Please check url.'
    gc.enable()

    try:
        # request the data from the given url
        r = requests.get(path_to_data)

        # converts byte-code to string
        content = r.content.decode('utf-8')

        if content == None:
            return no_content_error_message    
        elif path.exists(file_name):
            curr_file_size = path.getsize(file_name)
            df = pd.read_csv(io.StringIO(content))
            df.to_csv('../data/latest_crime_data.csv', index=False)
            del df
            gc.collect()
            new_file_size = path.getsize(file_name)
            print(f"The {file_name} already exists and has been overwritten.\n")
            print(f"Old file size: {curr_file_size}\n")
            print(f"New file size: {new_file_size}")
        else:
            df = pd.read_csv(io.StringIO(content))
            df.to_csv("../data/latest_crime_data.csv", index=False)
            new_file_size = path.getsize(file_name)
            print(f"A new file called {file_name} has been created.\n")
            print(f"The file size is: {new_file_size}")
    except Exception as e:
        print("Unable to fetch dataset from url.")
        print(e)