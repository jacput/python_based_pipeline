# SalesPipeline

## Overview

SalesPipeline is a Python-based ETL (Extract, Transform, Load) project that demonstrates a production-style data ingestion pipeline. The application reads sales data from a CSV file, validates the data, and loads it into a SQL Server staging table for downstream processing.

The project was designed using modular components and follows many of the same practices used in enterprise ETL solutions.

---

## Features

* Reads sales data from CSV files using pandas
* Configuration-driven application using JSON
* Validates required input columns before processing
* Loads data into SQL Server staging tables
* Adds metadata columns such as:

  * Source file name
  * Batch ID
  * Insert timestamp
* Batch processing for improved performance with large files
* Centralized logging
* Modular and maintainable project structure
* Uses SQLAlchemy with fast batch inserts

---

## Technologies

* Python 3.11
* pandas
* SQLAlchemy
* pyodbc
* Microsoft SQL Server
* JSON configuration
* Logging module

---

## Project Structure

```text
SalesPipeline/
│
├── config.py
├── config.json
├── csv_loader.py
├── database.py
├── logger.py
├── validator.py
├── main.py
├── requirements.txt
├── README.md
└── logs/
```

---

## Workflow

1. Read configuration settings.
2. Initialize logging.
3. Load the source CSV file.
4. Validate the required columns.
5. Add ETL metadata columns.
6. Upload records to the SQL Server staging table in batches.
7. Log completion or any processing errors.

---

## Configuration

Application settings are stored in `config.json`.

Typical configuration includes:

* Source file location
* Source file name
* SQL Server connection information
* Logging location
* Target staging table

The configuration file is excluded from source control so that sensitive information is not committed to GitHub.

---

## Batch Processing

To improve loading performance, records are uploaded in configurable batches instead of inserting rows one at a time.

This approach:

* Reduces memory usage
* Improves SQL Server insert performance
* Scales better for larger datasets

---

## Logging

The application generates log files that record:

* Application startup
* Validation results
* Records processed
* SQL load status
* Errors and exceptions

This makes troubleshooting significantly easier in production environments.

---

## Error Handling

The pipeline validates the input data before loading.

Examples include:

* Missing required columns
* File access errors
* SQL connection failures
* Database insert exceptions

Errors are logged with detailed information to simplify troubleshooting.

---

## Future Enhancements

Potential improvements include:

* Azure Data Factory orchestration
* Azure Blob Storage integration
* Automated bad-record handling
* Stored procedure execution after successful load
* Data quality reporting
* Unit tests
* CI/CD using GitHub Actions
* Docker containerization
* Support for multiple file formats

---

## Getting Started

### Clone the repository

```bash
git clone <repository-url>
cd SalesPipeline
```

### Create a virtual environment

```bash
python -m venv .venv
```

### Activate the virtual environment

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure the application

Update `config.json` with your local SQL Server and file paths.

### Run the pipeline

```bash
python main.py
```

---

## Skills Demonstrated

This project demonstrates practical experience with:

* Python application development
* ETL pipeline design
* SQL Server integration
* Data validation
* Batch processing
* Configuration management
* Logging
* Exception handling
* Modular software architecture
* Version control using Git

---

## License

This project is provided for educational and portfolio purposes.
