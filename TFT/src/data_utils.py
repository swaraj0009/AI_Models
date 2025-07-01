import os
import pandas as pd
import glob
from concurrent.futures import ThreadPoolExecutor

def set_working_directory(path="/home/jovyan/roc-qa-ai/AI_Driven_Resource_Forecasting"):
    """
    Sets the working directory to the specified path.

    Args:
        path (str): The path to set as the working directory. Defaults to '/home/jovyan/roc-qa-ai/AI_Driven_Resource_Forecasting'.

    Returns:
        str: The absolute path of the current working directory after setting it.
    """
    try:
        os.chdir(path)
        print(f"Working directory set to: {os.getcwd()}")
        return os.getcwd()
    except Exception as e:
        print(f"Error setting working directory: {e}")
        return None
    
BASE_DATA_DIR = "/home/jovyan/dataset"

def load_and_process_data(base_data_dir=BASE_DATA_DIR):
        """
        Loads and processes CSV files from the specified directory.

        Args:
            base_data_dir (str): The directory containing the CSV files.

        Returns:
            pd.DataFrame: A concatenated DataFrame with processed data.
        """
        
        def read_csv_with_vm(f):
            dfraw = pd.read_csv(f, sep=';', engine='c')  # Reads each CSV file with `;` as separator
            dfraw['VM'] = os.path.basename(f).split('.')[0]  # Adds a new column called `VM` using the filename
            return dfraw

        all_files = glob.glob(os.path.join(base_data_dir, "*.csv"))  # Get all CSV files in the directory

        with ThreadPoolExecutor() as executor:
            results = list(executor.map(read_csv_with_vm, all_files))  # Faster loading of many files

        dfraw = pd.concat(results, ignore_index=True)  # Concatenate all DataFrames into one

        dfraw.columns = dfraw.columns.str.strip().str.replace(';', '', regex=False)  # Clean column names: strip spaces + remove semicolons

        return dfraw