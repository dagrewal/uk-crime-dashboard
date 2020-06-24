import requests
import csv
from os import path

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
    try:
        r = requests.get(path_to_data)
        content = r.text

        if len(content) == 0:
            return 'No content has been downloaded!'    

        if path.exists(file_name):
            curr_file_size = path.getsize(file_name)

            with open(file_name, 'w') as csv_file:
                writer = csv.writer(csv_file)
                csv_file.write(content)
                #csv_file.write(reader)
                new_file_size = path.getsize(file_name)
                #csv_file.close()

            print(f"The {file_name} already exists and has been overwritten.\n")
            print(f"Old file size: {curr_file_size}\n")
            print(f"New file size: {new_file_size}")
        else:
            with open(file_name, 'w') as csv_file:
                reader = csv.reader(content.splitlines(), delimiter=',', quotechar='"')
                csv_file.write(reader)
                csv_file.close()

            new_file_size = path.getsize(file_name)
            print(f"A new file called {file_name} has been created.\n")
            print(f"The file size is: {new_file_size}")
    except Exception as e:
        print("Unable to read dataset.")
        print(e)