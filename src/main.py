import argparse
import json
import logging
import os
from datetime import datetime

import pandas as pd


def setup_logging():
    """Configure execution logging."""

    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(
        filename="logs/pipeline.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def load_config(config_path):
    """Load validation rules from a JSON configuration file."""

    try:
        with open(config_path, "r") as file:
            return json.load(file)

    except FileNotFoundError:
        logging.error("Configuration file not found: %s", config_path)
        print(f"Error: Configuration file '{config_path}' was not found.")
        return None

    except json.JSONDecodeError:
        logging.error("Invalid JSON configuration file: %s", config_path)
        print(f"Error: Configuration file '{config_path}' contains invalid JSON.")
        return None


def validate_required_columns(df, config):
    """Check whether all required columns exist in the dataset."""

    required_columns = config.get("required_columns", [])
    missing_columns = [
        column for column in required_columns if column not in df.columns
    ]

    return missing_columns


def validate_numeric_rules(df, config):
    """Check numeric columns against minimum and maximum rules."""

    numeric_rules = config.get("numeric_rules", {})
    validation_results = {}

    for column, rules in numeric_rules.items():
        if column not in df.columns:
            continue

        violations = 0

        if "min" in rules:
            violations += (df[column] < rules["min"]).sum()

        if "max" in rules:
            violations += (df[column] > rules["max"]).sum()

        validation_results[column] = int(violations)

    return validation_results


def generate_report(
    file_path,
    df,
    missing_columns,
    duplicate_count,
    empty_row_count,
    validation_results,
    rows_removed,
):
    """Generate a text report containing pipeline results."""

    os.makedirs("output", exist_ok=True)
    report_path = "output/data_quality_report.txt"

    with open(report_path, "w") as report:
        report.write("DATA QUALITY AUTOMATION REPORT\n")
        report.write("=" * 40 + "\n\n")

        report.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report.write(f"Input dataset: {file_path}\n\n")

        report.write("DATASET OVERVIEW\n")
        report.write("-" * 20 + "\n")
        report.write(f"Rows: {df.shape[0]}\n")
        report.write(f"Columns: {df.shape[1]}\n\n")

        report.write("MISSING VALUES\n")
        report.write("-" * 20 + "\n")
        for column, count in df.isnull().sum().items():
            report.write(f"{column}: {count}\n")

        report.write("\nQUALITY CHECKS\n")
        report.write("-" * 20 + "\n")
        report.write(f"Duplicate rows: {duplicate_count}\n")
        report.write(f"Completely empty rows: {empty_row_count}\n")

        report.write("\nCONFIGURATION VALIDATION\n")
        report.write("-" * 25 + "\n")

        if missing_columns:
            report.write(
                f"Missing required columns: {', '.join(missing_columns)}\n"
            )
        else:
            report.write("All required columns are present.\n")

        report.write("\nRULE-BASED VALIDATION\n")
        report.write("-" * 25 + "\n")

        if validation_results:
            for column, violations in validation_results.items():
                report.write(
                    f"{column}: {violations} rule violation(s)\n"
                )
        else:
            report.write("No numeric validation rules configured.\n")

        report.write("\nDATA CLEANING RESULTS\n")
        report.write("-" * 25 + "\n")
        report.write(f"Rows removed: {rows_removed}\n")

    return report_path


def analyze_and_clean_data(file_path, config):
    """Analyze, validate, clean, and report on a CSV dataset."""

    try:
        logging.info("Pipeline started for dataset: %s", file_path)

        print(
        "\nNote: Ensure that the JSON validation rules match the "
        "columns and data requirements of your dataset."
        )

        df = pd.read_csv(file_path)

        print("\n--- Dataset Overview ---")
        print(f"Rows: {df.shape[0]}")
        print(f"Columns: {df.shape[1]}")

        missing_columns = validate_required_columns(df, config)

        if missing_columns:
            logging.warning(
                "Dataset missing required columns: %s",
                ", ".join(missing_columns),
            )
            print(
                f"\nWarning: Missing required columns: "
                f"{', '.join(missing_columns)}"
            )

        print("\n--- Missing Values ---")
        print(df.isnull().sum())

        duplicate_count = int(df.duplicated().sum())
        empty_row_count = int(df.isnull().all(axis=1).sum())

        print("\n--- Duplicate Rows ---")
        print(f"Total duplicate rows: {duplicate_count}")

        print("\n--- Completely Empty Rows ---")
        print(f"Total completely empty rows: {empty_row_count}")

        validation_results = validate_numeric_rules(df, config)

        print("\n--- Rule-Based Validation ---")
        if validation_results:
            for column, violations in validation_results.items():
                print(f"{column}: {violations} rule violation(s)")
        else:
            print("No numeric validation rules configured.")

        # Safe data cleaning
        cleaned_df = df.drop_duplicates().dropna(how="all")
        rows_removed = len(df) - len(cleaned_df)

        os.makedirs("output", exist_ok=True)
        output_path = "output/cleaned_data.csv"
        cleaned_df.to_csv(output_path, index=False)

        # Generate report
        report_path = generate_report(
            file_path,
            df,
            missing_columns,
            duplicate_count,
            empty_row_count,
            validation_results,
            rows_removed,
        )

        logging.info(
            "Pipeline completed successfully. Rows removed: %s",
            rows_removed,
        )

        # Console notification
        print("\nPipeline completed successfully.")
        print(f"Cleaned dataset: {output_path}")
        print(f"Quality report: {report_path}")
        print("Execution details logged to: logs/pipeline.log")

    except FileNotFoundError:
        logging.error("Dataset file not found: %s", file_path)
        print(f"Error: Dataset '{file_path}' was not found.")

    except pd.errors.EmptyDataError:
        logging.error("The CSV dataset is empty: %s", file_path)
        print("Error: The CSV dataset is empty.")

    except Exception as error:
        logging.exception("Unexpected pipeline error")
        print(f"An unexpected error occurred: {error}")


def main():
    """Parse command-line arguments and start the pipeline."""

    setup_logging()

    parser = argparse.ArgumentParser(
        description="Data Quality Automation Tool"
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to the CSV dataset",
    )

    parser.add_argument(
        "--config",
        required=True,
        help="Path to the JSON validation configuration",
    )

    args = parser.parse_args()

    config = load_config(args.config)

    if config is not None:
        analyze_and_clean_data(args.input, config)


if __name__ == "__main__":
    main()