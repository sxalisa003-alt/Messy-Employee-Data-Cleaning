# Employee Dataset — Transformation Log

## 1. Overview

This document records the transformations applied to the synthetic HR employee dataset after the initial data-quality screening.

The cleaning process followed three principles:

1. Correct issues that can be objectively fixed.
2. Restructure data where the original format limits analysis.
3. Preserve missing or incomplete information when it cannot be reliably reconstructed.

The raw dataset contained **1,020 rows and 12 columns**.

After transformation, the dataset contained **1,020 rows and 13 columns**.

---

# 2. Department and Region Transformation

### Issue

The original dataset stored department and region together in a single column:

```text
department_region
```

Example structure:

```text
DevOps-California
Finance-Texas
Admin-Nevada
```

### Transformation

The combined field was split into two separate columns:

```python
df[['department', 'region']] = df['department_region'].str.split('-', expand=True)
```

The resulting columns were:

```text
department
region
```

The original `department_region` column was then removed:

```python
df = df.drop(columns='department_region')
```

### Validation

The transformation was checked by reconstructing the original values:

```python
(df['department_region'] == df['department'] + '-' + df['region']).all()
```

Result:

```text
True
```

Both new columns contained zero missing values.

### Outcome

The dataset now contains department and region as independent fields, making them easier to use for grouping, filtering, reporting and visualisation.

---

# 3. Join Date Transformation

### Issue

`join_date` was stored as a text/object field rather than a datetime field.

### Transformation

The column was converted using pandas:

```python
df['join_date'] = pd.to_datetime(df['join_date'])
```

### Validation

The conversion was tested before applying it to the DataFrame.

The resulting data type was:

```text
datetime64[ns]
```

No dates became missing during conversion.

The resulting date range was:

```text
Minimum: 2020-01-01
Maximum: 2024-12-29
```

### Outcome

`join_date` is now stored as a proper datetime field and can be used for time-based analysis.

---

# 4. Email Transformation

### Issue

The original email field contained repeated email addresses.

There were:

```text
1,020 employee records
64 unique email addresses
```

The repeated emails did not correspond to duplicate employee records because employee IDs remained unique.

For this synthetic dataset, a unique email identifier was therefore created for each employee.

### Department Code

The first letter of each department was used as a department code.

Examples:

```text
Admin       → A
Cloud Tech  → C
DevOps      → D
Finance     → F
HR          → H
Sales       → S
```

```python
dept_code = df['department'].str[0].str.upper()
```

### Region Code

An explicit mapping was used to avoid collisions between regions beginning with the same letter.

```python
region_map = {
    'California': 'CA',
    'Florida': 'FL',
    'Illinois': 'IL',
    'Nevada': 'NV',
    'New York': 'NY',
    'Texas': 'TX'
}

reg_code = df['region'].map(region_map)
```

The mapping produced zero missing region codes.

### Employee Number

The numeric portion of the existing employee ID was extracted:

```python
emp_num = df['employee_id'].str[3:]
```

The department, region and employee number were then combined:

```python
employee_code = dept_code + reg_code + emp_num
```

Examples:

```text
DCA1000
FTX1001
ANV1002
ANV1003
CFL1004
```

### New Email Structure

The employee code was incorporated into the existing email structure to create a unique synthetic identifier.

Examples:

```text
bob.davis_DCA1000@example.com
bob.brown_FTX1001@example.com
alice.jones_ANV1002@example.com
```

### Validation

The generated employee codes were checked for:

```text
Missing employee codes: 0
Unique employee codes: 1,020
```

The generated email values were checked for:

```text
Missing emails: 0
Unique emails: 1,020
```

All generated addresses retained the `example.com` domain.

### Outcome

The email field now contains a unique synthetic identifier for each employee.

> **Note:** These are synthetic identifiers created for this portfolio dataset. They are not verified employee email addresses.

---

# 5. Phone Number Transformation

### Issue

The original phone values were stored as integers and contained negative signs.

All 1,020 original values were negative.

Further inspection showed inconsistent digit lengths:

| Digit Length | Records |
| ------------ | ------: |
| 10           |     928 |
| 9            |      78 |
| 8            |      12 |
| 7            |       2 |

Therefore, 92 records contained incomplete phone numbers.

### Transformation

The phone column was converted to strings and the invalid negative sign was removed:

```python
phone_test = df['phone'].astype(str).str.replace('-', '', regex=False)
```

Values shorter than 10 digits were identified:

```python
invalid_phone = phone_test.str.len() < 10
```

Incomplete values were then marked as missing:

```python
df['phone'] = phone_test
df.loc[invalid_phone, 'phone'] = pd.NA
df['phone'] = df['phone'].astype('string')
```

### Validation

Final phone values were checked for:

- Missing values
- Digit length
- Data type

Final result:

```text
Valid 10-digit numbers: 928
Missing/incomplete numbers: 92
Data type: string
```

### Outcome

The invalid negative formatting was removed from usable phone numbers.

Incomplete numbers were not padded or artificially reconstructed.

The 92 incomplete values were preserved as missing.

---

# 6. Missing Age Values

### Issue

There were 211 missing age values.

The observed ages were:

```text
25
30
35
40
```

No reliable information was available to determine the missing ages.

### Transformation

No values were imputed.

The missing values were intentionally preserved:

```text
211 missing values
```

### Reason

Replacing missing ages with the mean, median or another arbitrary value would introduce information that was not present in the original dataset.

### Outcome

The `age` column remains partially incomplete but retains the original information accurately.

---

# 7. Missing Salary Values

### Issue

There were 24 missing salary values.

Salary distributions were examined across the available employee attributes, including:

- Department
- Status
- Performance score
- Remote work
- Overall salary distribution

No reliable relationship was found that would allow the missing salaries to be reconstructed.

### Transformation

No imputation was performed.

The 24 missing salaries were preserved as missing values.

### Reason

An unknown salary should not be interpreted as:

```text
0
```

or automatically replaced with the:

```text
mean
median
```

Doing so could distort salary statistics and introduce assumptions into later analysis.

### Outcome

The 24 missing salary values remain explicitly missing.

---

# 8. Categorical Fields

The following categorical fields were inspected and did not require transformation:

### Status

Valid categories:

```text
Active
Pending
Inactive
```

### Performance Score

Valid categories:

```text
Poor
Average
Good
Excellent
```

### Remote Work

Values:

```text
True
False
```

The `remote_work` field was already stored as a Boolean (`bool`) and contained no missing values.

### Outcome

No unnecessary transformations were applied to these fields.

---

# 9. Employee IDs and Duplicate Records

No transformation was required for employee identifiers.

Validation showed:

```text
Total rows: 1,020
Unique employee IDs: 1,020
Missing employee IDs: 0
Duplicate employee IDs: 0
```

Exact duplicate records were also checked:

```text
Exact duplicate rows: 0
```

### Outcome

No employee records were removed.

---

# 10. Names

The `first_name` and `last_name` columns were checked for:

- Leading/trailing whitespace
- Obvious casing inconsistencies
- Unexpected values
- Formatting issues

No issues requiring transformation were identified.

### Outcome

Names were retained in their original form.

---

# 11. Final Data Structure

After all transformations, the dataset contains:

**1,020 rows × 13 columns**

Final columns:

```text
employee_id
first_name
last_name
age
status
join_date
salary
email
phone
performance_score
remote_work
department
region
```

Final data types:

| Column              | Data Type      |
| ------------------- | -------------- |
| `employee_id`       | object         |
| `first_name`        | object         |
| `last_name`         | object         |
| `age`               | float64        |
| `status`            | object         |
| `join_date`         | datetime64[ns] |
| `salary`            | float64        |
| `email`             | object         |
| `phone`             | string         |
| `performance_score` | object         |
| `remote_work`       | bool           |
| `department`        | object         |
| `region`            | object         |

---

# 12. Final Missing Values

After transformation, the remaining missing values were:

| Column            | Missing Values | Reason                              |
| ----------------- | -------------: | ----------------------------------- |
| `age`             |            211 | Could not be reliably reconstructed |
| `salary`          |             24 | Could not be reliably reconstructed |
| `phone`           |             92 | Original values were incomplete     |
| All other columns |              0 | —                                   |

These missing values are intentional and documented rather than being unresolved cleaning errors.

---

# 13. Transformation Summary

| Field / Issue       | Transformation                       | Result                    |
| ------------------- | ------------------------------------ | ------------------------- |
| `department_region` | Split into two columns               | `department` + `region`   |
| `join_date`         | Converted to datetime                | `datetime64[ns]`          |
| `email`             | Created unique synthetic identifiers | 1,020 unique values       |
| `phone`             | Removed negative sign                | 928 valid 10-digit values |
| Incomplete phones   | Marked as missing                    | 92 missing                |
| `age`               | No imputation                        | 211 missing retained      |
| `salary`            | No imputation                        | 24 missing retained       |
| `employee_id`       | Validated                            | 1,020 unique              |
| Duplicate rows      | Validated                            | 0                         |
| `status`            | Validated                            | No change                 |
| `performance_score` | Validated                            | No change                 |
| `remote_work`       | Validated                            | No change                 |
| Names               | Validated                            | No change                 |

---

# 14. Final Validation

The cleaned DataFrame was checked after all transformations.

Final structure:

```text
Rows: 1,020
Columns: 13
```

Final duplicate check:

```text
Exact duplicate rows: 0
```

Final employee ID check:

```text
Unique employee IDs: 1,020
```

Final missing-value check confirmed that only the intentionally preserved missing values remained:

```text
age       211
salary     24
phone      92
```

---

# 15. Transformation Outcome

The dataset was successfully transformed from a **1,020 × 12 raw dataset** into a **1,020 × 13 cleaned dataset**.

The final dataset has:

- Separate department and region dimensions
- Proper datetime representation
- Unique synthetic employee email identifiers
- Standardised phone formatting
- Explicitly preserved incomplete information
- Validated employee identifiers
- No exact duplicate records
- Appropriate data types for analysis

The cleaned dataset is now ready for **exploratory analysis, SQL analysis and Power BI reporting**.
