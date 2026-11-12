import os
import pandas as pd


def analyze_and_clean_data(file_path):
    """Analyze a CSV file and create a safely cleaned copy."""

    try:
        # Load the dataset
        df = pd.read_csv(file_path)

        # ---------------- Dataset Analysis ----------------
        print("\n--- Dataset Overview ---")
        print(f"Rows: {df.shape[0]}")
        print(f"Columns: {df.shape[1]}")

        print("\n--- Column Data Types ---")
        print(df.dtypes)

        print("\n--- Missing Values ---")
        print(df.isnull().sum())

        duplicate_count = df.duplicated().sum()
        empty_row_count = df.isnull().all(axis=1).sum()

        print("\n--- Duplicate Rows ---")
        print(f"Total duplicate rows: {duplicate_count}")

        print("\n--- Completely Empty Rows ---")
        print(f"Total completely empty rows: {empty_row_count}")

        print("\n--- Numeric Data Summary ---")
        print(df.describe())

        # ---------------- Safe Data Cleaning ----------------
        cleaned_df = df.drop_duplicates()
        cleaned_df = cleaned_df.dropna(how="all")

        rows_removed = len(df) - len(cleaned_df)

        # Create output directory if it doesn't exist
        os.makedirs("output", exist_ok=True)

        output_path = "output/cleaned_data.csv"
        cleaned_df.to_csv(output_path, index=False)

        print("\n--- Data Cleaning Results ---")
        print(f"Rows removed: {rows_removed}")
        print(f"Cleaned dataset saved to: {output_path}")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")

    except pd.errors.EmptyDataError:
        print("Error: The CSV file is empty.")

    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    file_path = "data/sample/sample_data.csv"
    analyze_and_clean_data(file_path)