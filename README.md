# TPC-DS Dataset Using SQLAlchemy ORM

## 1. Project Overview

This project focuses on working with the TPC-DS benchmark dataset using MySQL and SQLAlchemy ORM.
The TPC-DS dataset is imported into a MySQL database, and SQLAlchemy ORM is used to perform SQL operations through Python.
The project aims to understand database operations and their equivalent implementations using SQLAlchemy ORM.

## 2. Technologies Used

- Python 3.12
- MySQL 8.0.43
- SQLAlchemy
- PyMySQL (if configured as the database driver)
- Git & GitHub
- VS Code

## 3. Dataset Information

The TPC-DS dataset contains multiple tables representing business data related to sales, customers, products, stores, catalogs and web transactions.
The dataset includes tables such as:
- customer
- customer_address
- customer_demographics
- date_dim
- item
- store
- store_sales
- store_returns
- catalog_sales
- catalog_returns
- web_sales
- web_returns
- web_site
- inventory
- warehouse
- promotion
- time_dim

## 4. Project Structure

```text
tpcds_orm/
│
├── database.py
├── models.py
├── queries.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## 5. Dataset Download and MySQL Import

### Step 1: Download the Dataset

The TPC-DS dataset was downloaded from the TPC-DS data repository.

The downloaded dataset was extracted into a local directory containing multiple `.dat` files.

Each `.dat` file represents the data corresponding to a particular TPC-DS table.

### Step 2: Create the MySQL Database

Open MySQL Command Line Client and execute:

```sql
CREATE DATABASE tpcds;

USE tpcds;
```

### Step 3: Import the TPC-DS Schema

The `tpcds.sql` schema file was obtained from the DSGen software package (`DSGen-software-code-4.0.0`).

The schema was imported into MySQL using PowerShell:

```powershell
Get-Content "path/to/tpcds.sql" | mysql -u root -p tpcds
```

This created the required TPC-DS tables in the database.

### Step 4: Enable Local Data Import

To allow local data loading, check the MySQL configuration:

```sql
SHOW VARIABLES LIKE 'local_infile';
```

If disabled, enable it:

```sql
SET GLOBAL local_infile = 1;
```

### Step 5: Import the .dat Files into MySQL

The extracted `.dat` files were loaded into their corresponding MySQL tables.

The data import process involved:

1. Selecting the appropriate `.dat` file.
2. Identifying its corresponding MySQL table.
3. Loading the records into the table.
4. Repeating the process for the remaining dataset files.

The schema file created the tables, while the `.dat` files populated them with actual records.

### Step 6: Verify the Imported Data

After importing the dataset, the records were verified using SQL queries:

```sql
USE tpcds;

SELECT COUNT(*) FROM customer;

SELECT COUNT(*) FROM store_sales;

SELECT COUNT(*) FROM date_dim;

SELECT COUNT(*) FROM item;
```

To view sample records:

```sql
SELECT * FROM customer LIMIT 5;

SELECT * FROM store_sales LIMIT 5;
```

## 6. SQLAlchemy ORM Implementation

SQLAlchemy ORM is used to interact with the MySQL database through Python.

The implementation involves:

- Creating a SQLAlchemy database engine.
- Establishing a MySQL database connection.
- Creating ORM models corresponding to database tables.
- Using sessions to execute ORM queries.
- Retrieving and processing query results.


## 7. Installation and Execution

### Step 1: Clone the Repository

```bash
git clone <repository-url>
```

### Step 2: Navigate to the Project Directory

```bash
cd tpcds_orm
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate the Virtual Environment

For Windows:

```bash
venv\Scripts\activate
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Configure Database Connection

Configure the MySQL database credentials in the `.env` file.

Ensure that the MySQL server is running and the TPC-DS dataset has been imported.

### Step 7: Execute the Queries

```bash
python queries.py
```

## 9. Future Enhancements

- Implement remaining SQL operations using SQLAlchemy ORM.
- Add advanced queries and window functions.
- Implement unit testing for ORM queries.
- Improve query performance and reusability.

---
**Project:** TPC-DS Dataset Using SQLAlchemy ORM
