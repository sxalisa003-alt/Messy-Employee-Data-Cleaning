# Employee Dataset — Data Screening

## 1. Overview

This document records the initial data-quality screening performed on a synthetic HR employee dataset before any transformations were applied.

The purpose of the screening stage was to:

- Understand the structure of the dataset
- Identify missing values
- Check data types
- Identify potential duplicates
- Inspect categorical fields
- Identify formatting and structural issues
- Determine which issues required cleaning

The screening was performed using **Python and pandas**.

---

## 2. Initial Dataset

The raw dataset contained:

- **Rows:** 1,020
- **Columns:** 12

Initial columns:

```text
employee_id
first_name
last_name
age
department_region
status
join_date
salary
email
phone
performance_score
remote_work
```

The initial data types included text (`object`), numerical values (`float64`/`int64`) and Boolean values.

---

## 3. Missing Value Screening

Missing values were checked across all columns using:

```python
df.isna().sum()
```

The following missing values were identified:

| Column            | Missing Values | Initial Assessment     |
| ----------------- | -------------: | ---------------------- |
| `age`             |            211 | Requires investigation |
| `salary`          |             24 | Requires investigation |
| All other columns |              0 | No missing-value issue |

### Age

The `age` column contained four observed age values:

```text
25
30
35
40
```

along with 211 missing values.

No additional information was available to reliably reconstruct the missing ages.

**Screening decision:** Investigate further during cleaning; do not automatically replace missing values.

### Salary

There were 24 missing salary values.

Salary statistics were examined to understand the distribution and determine whether the missing values could be reasonably inferred.

Summary statistics included:

- Minimum: approximately 50,047
- Median: approximately 85,548
- Mean: approximately 85,155
- Maximum: approximately 119,972

No negative or zero salary values were identified.

The missing salaries did not show an obvious relationship with department, status, performance score or remote-work status.

**Screening decision:** Missing salaries cannot be reliably reconstructed and should be preserved as missing.

---

## 4. Employee ID Screening

Employee IDs were checked for uniqueness and missing values.

```python
df['employee_id'].nunique()
df['employee_id'].isna().sum()
df['employee_id'].duplicated().sum()
```

Results:

| Check               | Result |
| ------------------- | -----: |
| Total rows          |  1,020 |
| Unique employee IDs |  1,020 |
| Missing IDs         |      0 |
| Duplicate IDs       |      0 |

Every employee record had a unique identifier.

**Screening decision:** No issue identified.

---

## 5. Duplicate Record Screening

Exact duplicate rows were checked using:

```python
df.duplicated().sum()
```

Result:

```text
0
```

No completely duplicated employee records were identified.

It was also noted that repeated values in individual fields, such as names, salaries or email addresses, do not automatically indicate duplicate employee records.

**Screening decision:** No records should be removed for exact duplication.

---

## 6. Department and Region Screening

The `department_region` field stored two pieces of information in a single column.

The field contained combinations of department and region, such as:

```text
DevOps-California
Finance-Texas
Admin-Nevada
```

Six departments and six regions were identified.

### Departments

```text
Admin
Cloud Tech
DevOps
Finance
HR
Sales
```

### Regions

```text
California
Florida
Illinois
Nevada
New York
Texas
```

The field therefore contained **36 department-region combinations**.

**Screening finding:** The field is structurally valid but combines two separate business dimensions.

**Screening decision:** Split `department_region` into separate `department` and `region` columns during transformation.

---

## 7. Status Screening

The `status` column contained three categories:

| Status   | Records |
| -------- | ------: |
| Pending  |     356 |
| Active   |     352 |
| Inactive |     312 |

Missing values:

```text
0
```

No unexpected categories were identified.

**Screening decision:** No transformation required.

---

## 8. Performance Score Screening

The `performance_score` column contained four categories:

| Performance Score | Records |
| ----------------- | ------: |
| Good              |     270 |
| Average           |     267 |
| Excellent         |     267 |
| Poor              |     216 |

Missing values:

```text
0
```

The values represent categorical performance ratings rather than continuous numerical scores.

**Screening decision:** No transformation required.

---

## 9. Remote Work Screening

The `remote_work` column contained:

| Remote Work | Records |
| ----------- | ------: |
| `True`      |     513 |
| `False`     |     507 |

Missing values:

```text
0
```

Data type:

```text
bool
```

The field was already appropriately represented as a Boolean variable.

**Screening decision:** No transformation required.

---

## 10. Join Date Screening

The `join_date` column was initially stored as an `object` (text) field.

The dates followed a consistent month/day/year format.

A conversion test was performed:

```python
test_dates = pd.to_datetime(df['join_date'])
```

The test produced:

```text
datetime64[ns]
```

and resulted in:

```text
0
```

missing dates.

The observed date range was:

```text
Minimum: 2020-01-01
Maximum: 2024-12-29
```

**Screening finding:** The dates appear valid but are stored using an inappropriate data type for date analysis.

**Screening decision:** Convert `join_date` to a pandas datetime field.

---

## 11. Email Screening

The email field was investigated for uniqueness.

Results:

```text
Employee records: 1,020
Unique email addresses: 64
```

This meant that many employee records shared the same email address.

Further investigation showed that repeated email addresses could occur across different employee IDs and employee attributes.

For example, the same email could appear for multiple distinct employee records.

This was treated as a **data-quality issue with the email field**, rather than evidence of duplicate employees.

**Screening decision:** Investigate whether unique synthetic identifiers can be created while preserving the employee relationship.

---

## 12. Phone Number Screening

The `phone` column was initially stored as an integer field.

Initial inspection showed:

- 1,020 non-null values
- 0 missing values
- All values were negative
- Phone numbers had inconsistent digit lengths

The negative sign was identified as an invalid formatting characteristic.

After removing the negative sign for inspection, digit lengths were:

| Digit Length | Records |
| ------------ | ------: |
| 10 digits    |     928 |
| 9 digits     |      78 |
| 8 digits     |      12 |
| 7 digits     |       2 |

Therefore:

- **928** values contained 10 digits
- **92** values were incomplete

The incomplete values could not be reliably reconstructed from the available data.

**Screening decision:**

- Remove the invalid negative sign during cleaning
- Preserve valid 10-digit numbers
- Treat incomplete phone numbers as missing
- Do not invent or pad missing digits

---

## 13. Name Screening

The `first_name` and `last_name` fields were inspected for:

- Unexpected values
- Inconsistent capitalization
- Leading/trailing whitespace
- Obvious formatting problems

The observed names were consistently formatted.

Whitespace checks confirmed that the values did not contain unnecessary leading or trailing spaces.

Repeated names were not treated as duplicates because names are not unique employee identifiers.

**Screening decision:** No transformation required.

---

# 14. Screening Summary

The initial screening identified the following data-quality issues:

| Issue                      | Finding                               | Planned Action                      |
| -------------------------- | ------------------------------------- | ----------------------------------- |
| Missing ages               | 211                                   | Preserve as missing                 |
| Missing salaries           | 24                                    | Preserve as missing                 |
| Combined department/region | 1 field containing 2 dimensions       | Split into separate columns         |
| Join dates                 | Stored as text                        | Convert to datetime                 |
| Email uniqueness           | 64 unique emails across 1,020 records | Create unique synthetic identifiers |
| Phone formatting           | Negative values                       | Remove invalid sign                 |
| Incomplete phone numbers   | 92 records                            | Preserve as missing                 |
| Employee IDs               | 1,020 unique                          | No action                           |
| Exact duplicates           | 0                                     | No action                           |
| Status                     | Valid categories                      | No action                           |
| Performance score          | Valid categories                      | No action                           |
| Remote work                | Boolean, no missing values            | No action                           |
| Names                      | No obvious formatting issues          | No action                           |

---

# 15. Screening Outcome

The screening stage established that the dataset was structurally usable but contained several data-quality issues requiring transformation.

The most important principle carried forward into the cleaning stage was:

> **Only make changes that can be supported by the available data.**

Missing information was not automatically replaced simply to eliminate null values. Where the original information could not be reliably reconstructed, the missing value was retained.

The identified issues were then addressed during the **data transformation and cleaning stage**.
