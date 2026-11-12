import pandas as pd


def analyze_data(file_path):
    """Load a CSV file and display basic data quality information."""

    try:
        # Load the dataset
        df = pd.read_csv(file_path)

        print("\n--- Dataset Overview ---")
        print(f"Rows: {df.shape[0]}")
        print(f"Columns: {df.shape[1]}")

        print("\n--- Column Data Types ---")
        print(df.dtypes)

        print("\n--- Missing Values ---")
        print(df.isnull().sum())

        print("\n--- Duplicate Rows ---")
        print(f"Total duplicate rows: {df.duplicated().sum()}")

        # Add these new sections here
        print("\n--- Completely Empty Rows ---")
        print(f"Total completely empty rows: {df.isnull().all(axis=1).sum()}")

        print("\n--- Numeric Data Summary ---")
        print(df.describe())

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")

    except pd.errors.EmptyDataError:
        print("Error: The CSV file is empty.")

    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    file_path = "data/sample/sample_data.csv"
    analyze_data(file_path)