import requests
import io
from os import path
import pandas as pd
import plotly.graph_objs as go

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

    try:
        # request the data from the given url
        r = requests.get(path_to_data)

        # converts byte-code to string
        content = r.content.decode('utf-8')

        if content == None:
            return no_content_error_message
        else:    
            df = pd.read_csv(io.StringIO(content))
            return df
    except Exception as e:
        print("Unable to fetch dataset from url.")
        print(e)

def clean_data():
    """
    Clean the data of redundant columns, missing values, data quality etc.

    Args:
        None

    Returns:
        df (pandas.DataFrame) containing cleaned version of data.
    """
    # url where data source is located
    csv_url = "https://www.ethnicity-facts-figures.service.gov.uk/crime-justice-and-the-law/policing/number-of-arrests/latest/downloads/number-of-arrests.csv"


    # call read_data()
    df = fetch_data(csv_url)

    # strip any whitespace in column names
    df.columns = [i.strip() for i in df.columns]

    # remove columns with low cardinality
    low_card_cols = df.columns[df.nunique() == 1].tolist()
    if low_card_cols != []:
        df.drop(low_card_cols, axis=1, inplace=True)
    else:
        del low_card_cols

    # remove notes column due to number of missing values. This may change in future.
    df.drop(['Notes'], axis=1, inplace=True)

    # drop ethnicity type as it is completely correlated with ethnicity
    df.drop(['Ethnicity_type'], axis=1, inplace=True)

    # sort data by time
    df.sort_values(by='Time', ascending=True, inplace=True)
    df.reset_index(drop=True, inplace=True)

    # clean the number of arrests by removing commas from numbers and removing non-numeric chars
    df['Number of arrests'] = df['Number of arrests'].str.replace("[^0-9]", "").str.strip()

    # create a flag column to show rows with missing values in number of arrests
    df['Missing_Number_of_Arrests'] = df['Number of arrests'].apply(lambda x: 1 if x == '' else 0)

    # convert arrests column to int
    df['Number of arrests'] = df['Number of arrests'].replace('', -1)
    df['Number of arrests'] = df['Number of arrests'].astype(int)

    

    return df

def filter_df(how='all'):
    """
    Filters the data to include only stats about population as a whole.

    Args:
        how (string) ['all', 'not all'] representing how to filter the data:
            'all' selects all rows where column values = all
            'not all' selects all rows where column values != all 

    Returns:
        filtered_df (pandas.DataFrame) containing filtered data
    """
    # call clean_data()
    df = clean_data()

    if how == 'all':
        filtered_df = df.loc[(df.Geography=='All') & (df.Gender=='All') & (df.Ethnicity=='All') &
                             (df.Age_Group=='All') & (df.Missing_Number_of_Arrests == 0)].copy()
    elif how == 'not all':
        filtered_df = df.loc[(df.Ethnicity != 'All') & (df.Gender != 'All') &
                             (df.Age_Group != 'All') & (df.Geography != 'All') &
                             (df.Missing_Number_of_Arrests == 0)].copy()
    else:
        raise Exception("Parameter value not recognised. Value must be 'all' or 'not all'.")

    return filtered_df

def plot_data():
    """
    Plots the data to be displayed on the frontend of the web application.

    Args:
        None

    Returns:
        figures (list) containing the plotly visualisations (dict)
    """
    # call clean_data()
    df_all = filter_df()
    df_not_all = filter_df(how='not all')

    # plot the total number of arrests over time
    plot_one = []
    x_vals = df_all.groupby('Time')['Number of arrests'].sum().index.tolist()
    y_vals = df_all.groupby('Time')['Number of arrests'].sum().tolist()

    plot_one.append(
        go.Scatter(
            x=x_vals,
            y=y_vals,
            mode='lines+markers',
            marker=dict(
                symbol=200
            ),
            name='Number of arrests',
            line=dict(
                color="rgb(34, 204, 207)"
            )
        )
    )

    layout_one = dict(
        title="Number of Total Arrests per Year",
        font =dict(
            color="white"
        ),
        plot_bgcolor='transparent',
        paper_bgcolor="transparent",
        xaxis=dict(
            title='Year',
            color='white',
            showgrid=False
        ),
        yaxis=dict(
            title="Number of arrests",
            color='white'
        ),
    )

    # plot the number of arrests by age group and gender
    gender_age_groups = df_not_all.groupby(['Age_Group', 'Gender'])['Number of arrests'].sum()
    age_groups = gender_age_groups.index.get_level_values(0).tolist()
    female_arrests = gender_age_groups[gender_age_groups.index.get_level_values(1) == 'Female'].values.tolist()
    male_arrests = gender_age_groups[gender_age_groups.index.get_level_values(1) == 'Male'].values.tolist()

    plot_two = []

    plot_two.append(
        go.Bar(
            name='Female',
            x=age_groups,
            y=female_arrests
        )
    )
    plot_two.append(
        go.Bar(
            name='Male',
            x=age_groups,
            y=male_arrests
        )
    )

    layout_two = dict(
        title="Number of Arrests by Age Group & Gender",
        font=dict(
            color='white'
        ),
        plot_bgcolor='transparent',
        paper_bgcolor='transparent',
        xaxis=dict(
            color='white'
        ),
        yaxis=dict(
            color='white',
            title='Number of arrests'
        ),
        barmode='group'
    )

    


    # append all plotly graphs to a list
    figures = []
    figures.append(dict(data=plot_one, layout=layout_one))
    figures.append(dict(data=plot_two, layout=layout_two))

    return figures
    
    

"""
business questions:
number of arrests per force
number of arrests by age group
number of arrests by time
number of arrests by ethnicity
"""