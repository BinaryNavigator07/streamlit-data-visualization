import pandas as pd
import streamlit as st
import os
from pathlib import Path

# Using Streamlit's caching to speed up repeated data loading
@st.cache_data
def load_data(filename="pm25_cleaned.csv"):
    """
    This function loads the cleaned PM2.5 dataset.
    It also extracts the 'Year' from the 'Period' column and adds it as a new column.
    
    The function tries multiple possible paths to find the data file, making it
    work both locally and in cloud deployments.

    Parameters:
    - filename: The name of the CSV file containing the cleaned dataset

    Returns:
    - df: The cleaned DataFrame with an additional 'Year' column
    """
    # Try multiple possible paths to find the data
    possible_paths = [
        f"../data/processed/{filename}",  # Relative path from streamlit_app directory
        f"./data/processed/{filename}",   # Relative path from project root
        f"{os.path.join(os.path.dirname(__file__), '../../data/processed', filename)}",  # Absolute path
    ]
    
    # Try each path until we find the file
    for filepath in possible_paths:
        try:
            st.write(f"Trying to load data from: {filepath}")
            df = pd.read_csv(filepath)
            st.success(f"Successfully loaded data from: {filepath}")
            break
        except FileNotFoundError:
            continue
    else:  # This runs if the for loop completes without a break (i.e., all paths failed)
        # If all paths fail, show a helpful error message
        st.error(f"Could not find the data file '{filename}'. Please check that the data files exist.")
        # Create a sample dataframe with a warning message
        df = pd.DataFrame({
            'Country': ['Data file not found'],
            'Period': ['2022'],
            'Value': [0],
            'Message': ['Please run the notebooks to generate the data files or check repository structure']
        })
    
    # Convert the 'Period' column (which represents year in string format) to datetime and extract the year
    if 'Period' in df.columns:
        df['Year'] = pd.to_datetime(df['Period'], format='%Y').dt.year  # Only extract the year part
    
    # Return the dataframe with the new 'Year' column
    return df
