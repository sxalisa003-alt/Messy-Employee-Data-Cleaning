"""
screen_employee_data.py

Data-quality screening pipeline for the Messy_Employee_dataset.csv file.

This script is organized into stages:

    1. Config / file paths
    2. Load data
    3. Standardize column names
    4. Screening functions (read-only data-quality checks)
    5. Save the screened dataset

The screening functions investigate potential data-quality issues without
modifying the dataset. The findings from this stage will be used to determine
which issues can be objectively corrected during the cleaning stage.
"""

import pandas as pd

# 1. CONFIG


INPUT_PATH = (
   "C:/Users/kamva/OneDrive/Desktop/PORTFOLIO/Cleaning_Datasets/Mess_Employee_Dataset/Messy_Employee_dataset.csv"
)

OUTPUT_PATH = (
    "C:/Users/kamva/OneDrive/Desktop/PORTFOLIO/Cleaning_Datasets/Mess_Employee_Dataset/Screened_Employee_dataset.csv"
)

# 2. LOAD DATA

def load_data(path: str) -> pd.DataFrame:
    """Read the raw CSV file."""
    df = pd.read_csv(
        path,
        sep=",",
        encoding="utf-8",
    )

    return df

# 3. STANDARDIZE COLUMN NAMES

def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Strip whitespace, lowercase, and replace spaces with underscores."""
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    return df

# 4. SCREENING FUNCTIONS

# These checks investigate the data but do not intentionally modify df.

def screen_row_count(df: pd.DataFrame) -> None:
    """Display the dataset structure and row/column counts."""
    df.info()


def screen_phone_numbers(df: pd.DataFrame) -> pd.Series:
    """
    Inspect the phone column for formatting inconsistencies.

    The dataset contains negative integer values. After converting the values
    to strings, the digits after the hyphen are inspected to determine whether
    the numbers contain 10 digits or fewer.

    Returns:
        pd.Series: The extracted digit segment after the hyphen.
    """
    phone_as_str = df["phone"].astype(str)

    # Isolate everything after the first hyphen.
    split_num = phone_as_str.str.split("-").str[1]

    # Separate correctly-sized numbers from shortened numbers.
    digit_10 = split_num[split_num.str.len() == 10]
    short_digit = split_num[split_num.str.len() < 10]

    print(
        f"10 Digits sample:\n{digit_10.head(1)}\n\n"
        f"<10 Digits sample:\n{short_digit.head(1)}"
    )

    # Check whether shortened numbers cluster around particular
    # leading digits.
    first_digit_short = short_digit.str[0].value_counts()
    first_digit_10 = digit_10.str[0].value_counts()

    print(
        f"Short Numbers first digit counts:\n{first_digit_short}\n\n"
        f"10-Digit numbers first digit counts:\n{first_digit_10}"
    )

    # Check the numeric range of the 10-digit numbers.
    print(
        f"Min of 10-digit numbers: {digit_10.astype(int).min()}\n"
        f"Max of 10-digit numbers: {digit_10.astype(int).max()}"
    )

    return split_num


def screen_employee_id_and_email(df: pd.DataFrame) -> pd.DataFrame:
    """
    Investigate employee ID and email uniqueness by constructing a proposed
    employee-specific email identifier.

    The proposed identifier combines:
        - department initial
        - region initial
        - employee ID suffix

    This is an investigation only. The original email column is not changed.
    """
    dept_initial = df["department_region"].str[0].str.upper()

    region_initial = (
        df["department_region"]
        .str.split("-")
        .str[1]
        .str[0]
        .str.upper()
    )

    emp_id_suffix = df["employee_id"].str[4:]

    new_code = dept_initial + region_initial + emp_id_suffix

    new_email = (
        df["email"].str.split("@").str[0]
        + "_"
        + new_code
        + "@"
        + df["email"].str.split("@").str[1]
    )

    print(f"Unique new emails: {new_email.nunique()}")
    print(
        f"Unique email domains: "
        f"{new_email.str.split('@').str[1].nunique()}"
    )

    comparison = pd.DataFrame(
        {
            "old_email": df["email"],
            "new_email": new_email,
        }
    )

    print(comparison.head())

    return comparison


def screen_duplicates(df: pd.DataFrame) -> None:
    """Check employee IDs and emails for duplicate values."""
    unique_employee_ids = df["employee_id"].nunique()

    print(
        f"Unique employee IDs: {unique_employee_ids} "
        f"(total rows: {len(df)})"
    )

    if unique_employee_ids < len(df):
        print("Duplicates spotted in the employee_id column!")
    else:
        print("No duplicate employee IDs found.")

    dup_emails = df[df.duplicated(subset=["email"], keep=False)]

    print(f"Unique emails: {df['email'].nunique()}")
    print(f"Rows with duplicated emails: {len(dup_emails)}")

    print(dup_emails.head())


def screen_categorical_columns(df: pd.DataFrame) -> None:
    """Inspect distinct values and distributions of categorical columns."""
    print(f"Unique join dates: {df['join_date'].nunique()}")

    print("\nRemote Work:")
    print(df["remote_work"].unique())
    print(df["remote_work"].value_counts())

    print("\nPerformance Score:")
    print(df["performance_score"].unique())
    print(df["performance_score"].value_counts())

    print("\nStatus:")
    print(df["status"].unique())
    print(df["status"].value_counts())

    print("\nRegions:")
    print(df["department_region"].str.split("-").str[1].unique())

    print("\nDepartment & Region combinations:")
    print(df["department_region"].value_counts())


def screen_missing_and_summary(df: pd.DataFrame) -> None:
    """Inspect missing values and summary statistics."""
    cols = [
        "age",
        "department_region",
        "status",
        "performance_score",
        "remote_work",
    ]

    # Inspect records where salary is missing.
    result = df.loc[df["salary"].isna(), cols]

    print("Rows with missing salary:")
    print(result)

    print("\nAge distribution:")
    print(df["age"].value_counts())

    print("\nMissing values:")
    print(df.isna().sum())

    print("\nDescriptive statistics:")
    print(df.describe())

    print("\nDataFrame information:")
    df.info()


# 5. SAVE SCREENED DATA

def save_screened_data(df: pd.DataFrame, path: str) -> None:
    """Write the screened dataset to a new CSV file."""
    df.to_csv(
        path,
        index=False,
        encoding="utf-8",
    )

    print(f"Screened data saved to: {path}")

# MAIN

def main():
    df = load_data(INPUT_PATH)

    df = clean_column_names(df)

    # --- Screening step ---
    screen_phone_numbers(df)
    # screen_row_count(df)
    # screen_employee_id_and_email(df)
    # screen_duplicates(df)
    # screen_categorical_columns(df)
    # screen_missing_and_summary(df)

    # --- Save screened dataset ---
    save_screened_data(df, OUTPUT_PATH)


if __name__ == "__main__":
    main()

