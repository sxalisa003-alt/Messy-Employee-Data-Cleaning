"""
transform_employee_data.py

Cleaning stage for Screened_Employee_dataset.csv (the output of the
screening step). Applies fixes identified during screening and saves
the result to a new CSV.

Stages:
    1. Config / file paths
    2. Load data
    3. Split department_region into separate columns
    4. Convert join_date to datetime
    5. Clean phone numbers
    6. Rebuild standardized email addresses
    7. Save cleaned data to a new CSV
"""

import pandas as pd



# 1. CONFIG

INPUT_PATH = "C:/Users/kamva/OneDrive/Desktop/PORTFOLIO/Cleaning_Datasets/Mess_Employee_Dataset/Screened_Employee_dataset.csv"
OUTPUT_PATH = "C:/Users/kamva/OneDrive/Desktop/PORTFOLIO/Cleaning_Datasets/Mess_Employee_Dataset/Cleaned_Employee_dataset.csv"

# maps full region names to their standard two-letter codes for the email rebuild
REGION_MAP = {
    "California": "CA",
    "Florida": "FL",
    "Illinois": "IL",
    "Nevada": "NV",
    "New York": "NY",
    "Texas": "TX",
}


# 2. LOAD DATA

def load_data(path: str) -> pd.DataFrame:
    """Read the screened CSV (semicolon-delimited)."""
    df = pd.read_csv(
        path,
        sep=";",
        encoding="utf-8",
    )
    return df

# 3. SPLIT DEPARTMENT & REGION

def split_department_region(df: pd.DataFrame) -> pd.DataFrame:
    """Split 'department_region' (e.g. 'DevOps-Florida') into two separate columns."""
    df[["department", "region"]] = df["department_region"].str.split("-", expand=True)
    df = df.drop(columns="department_region")
    return df


# 4. JOIN DATE

def convert_join_date(df: pd.DataFrame) -> pd.DataFrame:
    """Convert 'join_date' from text to an actual datetime dtype."""
    df["join_date"] = pd.to_datetime(df["join_date"])
    return df


# 5. CLEAN PHONE NUMBERS

def clean_phone(df: pd.DataFrame) -> pd.DataFrame:
    """
    Strip hyphens from phone numbers and null out any that end up
    shorter than 10 digits (i.e. not a valid full number).
    """
    stripped_phone = df["phone"].astype(str).str.replace("-", "", regex=False)
    invalid_number = stripped_phone.str.len() < 10

    df["phone"] = stripped_phone
    df.loc[invalid_number, "phone"] = pd.NA
    df["phone"] = df["phone"].astype("string")
    return df



# 6. REBUILD EMAIL ADDRESSES

def rebuild_email(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rebuild each email as '<username>_<code>@<domain>', where code is:
    first letter of department + region code (from REGION_MAP) + employee_id (from index 3 onward).
    """
    dept_code = df["department"].str[0].str.upper()
    reg_code = df["region"].map(REGION_MAP)
    emp_num = df["employee_id"].str[3:]
    emp_code = dept_code + reg_code + emp_num

    user_name = df["email"].str.split("@").str[0]
    domain = df["email"].str.split("@").str[1]

    df["email"] = user_name + "_" + emp_code + "@" + domain
    return df


# 7. SAVE CLEANED DATA

def save_cleaned_data(df: pd.DataFrame, path: str) -> None:
    """Write the cleaned DataFrame out to a new CSV file."""
    df.to_csv(path, index=False, encoding="utf-8")
    print(f"Cleaned data saved to: {path}")



# MAIN

def main():
    df = load_data(INPUT_PATH)
    df = split_department_region(df)
    df = convert_join_date(df)
    df = clean_phone(df)
    df = rebuild_email(df)

    print(df.isna().sum())  # quick check for any remaining missing values

    save_cleaned_data(df, OUTPUT_PATH)


if __name__ == "__main__":
    main()
