# Redynox Python Developer Internship — Task 2 Report

**Project:** Data Quality Automation Tool  
**Intern:** Samir Chowdhary  
**Repository:** https://github.com/SamirChowdhary24/data-quality-automation-tool

---

## 1. Problem Statement

Analysts and engineering teams routinely receive CSV datasets from external sources containing missing values, duplicate records, empty rows, missing columns, or out-of-range numeric values. Manually inspecting each incoming file before analysis or reporting is repetitive, time-consuming, and prone to human error.

---

## 2. Solution Approach

To automate this workflow, I built a configurable, CLI-based Python automation pipeline (`src/main.py`) using `pandas`, `argparse`, `json`, `logging`, and `os`.

- **Generic & Configurable Design:** Dataset-specific requirements (required columns and numeric min/max bounds) are decoupled from the Python code and stored in external JSON configuration files (`config/`), allowing the tool to validate any CSV structure without code changes.
- **Safe Data Cleaning:** The pipeline removes exact duplicate rows and completely empty rows while preserving the original input dataset and avoiding destructive imputation of partial missing values.
- **Automated Outputs & Logging:** Each run generates a cleaned dataset (`output/cleaned_data.csv`), a timestamped summary report (`output/data_quality_report.txt`), execution logs (`logs/pipeline.log`), and console completion notifications.
- **Error Handling:** Gracefully handles missing CSV files, empty datasets, missing configuration files, invalid JSON, and unexpected exceptions without crashing.
- **Scheduling:** Configured with **Windows Task Scheduler** to run unattended on a daily schedule using the virtual environment's Python interpreter and CLI arguments.

---

## 3. Demonstration & Testing Results

| Test Scenario | Input / Config | Result |
| :--- | :--- | :--- |
| **Sample Dataset** | `sample_data.csv` + `validation_rules.json` | Detected 3 missing values and 1 duplicate row; removed 1 row; generated cleaned CSV and report. |
| **Invalid Data** | `invalid_data.csv` + `validation_rules.json` | Caught 2 `age` rule violations (`-10`, `150`) and 1 `purchase_amount` violation (`-500`). |
| **Real-World Dataset** | `titanic.csv` (891 rows, 12 cols) + `titanic_rules.json` | Processed with zero code changes; flagged 177 missing `Age`, 687 missing `Cabin`, and 2 missing `Embarked` values. |
| **Missing Columns** | `sample_data.csv` + `titanic_rules.json` | Logged warning listing all 6 missing required columns and completed safely. |
| **Missing File** | `nonexistent.csv` + `validation_rules.json` | Caught `FileNotFoundError`, logged error, and printed clean message. |
| **Scheduled Run** | Windows Task Scheduler (`Daily` trigger) | Executed unattended and returned `The operation completed successfully. (0x0)`. |

*(Screenshots of execution runs, generated reports, error handling, and Task Scheduler verification are stored in `docs/screenshots/`.)*