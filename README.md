# HR Employee Data Cleaning & Preparation

##  Business Scenario

An HR department received an employee master dataset intended for workforce reporting and analysis. Before the data could be used for dashboards and reporting, several data-quality issues were identified, including missing values, duplicated email addresses, incorrectly structured fields, inconsistent data types, and invalid phone numbers.

The goal was to clean and prepare the dataset while **preserving information that could not be reliably reconstructed**.

---

##  Key Data-Quality Issues

| Issue | Finding | Action |
|---|---|---|
| Missing Age | 211 missing | Retained as missing |
| Missing Salary | 24 missing | Retained as missing |
| Department & Region | Stored together | Split into separate columns |
| Join Date | Stored as `object` | Converted to datetime |
| Email | 64 unique emails for 1,020 employees | Created unique synthetic emails |
| Phone | All values negative; 92 shorter than 10 digits | Removed invalid sign; did not invent missing digits |
| Employee ID | 1,020 unique IDs | No change |
| Status | 3 consistent categories | No change |
| Performance Score | 4 consistent categories | No change |
| Remote Work | Boolean | No change |

---

##  Cleaning Principles

The dataset was cleaned according to three principles:

- **Correct** issues that could be objectively fixed.
- **Restructure** information that was stored inefficiently.
- **Preserve** missing or incomplete information when it could not be reliably reconstructed.

> Cleaning data does not mean forcing every value to be complete.

---

##  Planned Transformations

### Department & Region
`department_region` will be separated into:

- `department`
- `region`

### Join Date
Convert `join_date` from text to a proper datetime data type.

### Email
Create unique synthetic employee emails using information already available in the dataset.

Example:

`heidi.jones_DI019@example.com`

These are **synthetic identifiers**, not verified real employee email addresses.

### Phone
Remove the invalid negative sign from interpretable phone values.

The 92 shortened numbers will **not** be padded or reconstructed because the missing digits cannot be determined reliably.

### Age & Salary
Missing values will remain missing because there is insufficient information to accurately reconstruct them.

---

##  Final Objective

Produce a clean, analysis-ready HR dataset suitable for:

- Employee headcount analysis
- Salary analysis
- Department and regional reporting
- Performance analysis
- Remote-work analysis
- Power BI dashboards
