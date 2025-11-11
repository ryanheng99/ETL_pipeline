# ETL Pipeline

A robust and scalable ETL (Extract, Transform, Load) pipeline for automated data processing, transformation, and integration workflows.

## 🎯 Overview

This project provides a comprehensive ETL pipeline framework designed for efficient data extraction from multiple sources, transformation according to business rules, and loading into target systems. Built with modularity and scalability in mind for production-grade data engineering workflows.

## ✨ Features

- **Multi-Source Extraction** - Connect to various data sources (CSV, Excel, databases, APIs)
- **Flexible Transformations** - Apply data cleaning, aggregation, and business logic
- **Multiple Load Targets** - Output to databases, data warehouses, or file systems
- **Error Handling** - Comprehensive logging and exception management
- **Scheduling Ready** - Compatible with cron jobs, Airflow, or other orchestrators
- **Data Validation** - Built-in data quality checks and validation rules
- **Incremental Loading** - Support for full and incremental data loads
- **Performance Optimized** - Efficient processing for large datasets

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        EXTRACT                              │
├─────────────────────────────────────────────────────────────┤
│  Data Sources:                                              │
│  • CSV/Excel Files          • REST APIs                    │
│  • Relational Databases     • Cloud Storage (S3, Azure)    │
│  • SFTP/FTP Servers        • Web Scraping                  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      TRANSFORM                              │
├─────────────────────────────────────────────────────────────┤
│  Operations:                                                │
│  • Data Cleaning           • Type Conversion               │
│  • Filtering & Validation  • Aggregation                   │
│  • Joins & Merges         • Feature Engineering           │
│  • Deduplication          • Business Rules                 │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                         LOAD                                │
├─────────────────────────────────────────────────────────────┤
│  Targets:                                                   │
│  • Data Warehouses (Snowflake, Redshift, BigQuery)        │
│  • Databases (PostgreSQL, MySQL, SQL Server)               │
│  • File Systems (CSV, Parquet, JSON)                      │
│  • Cloud Storage (S3, Azure Blob, GCS)                    │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Getting Started

### Prerequisites

```bash
Python 3.8+
pandas
sqlalchemy
psycopg2-binary  # for PostgreSQL
pymysql          # for MySQL
requests         # for API calls
```

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ryanheng99/ETL_pipeline.git
   cd ETL_pipeline
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials and settings
   ```

## 📖 Usage

### Basic ETL Pipeline

```python
from etl_pipeline import ETLPipeline
from extractors import CSVExtractor, DatabaseExtractor
from transformers import DataCleaner, Aggregator
from loaders import DatabaseLoader

# Initialize pipeline
pipeline = ETLPipeline(name="sales_data_pipeline")

# Extract
csv_extractor = CSVExtractor(file_path="data/sales.csv")
data = csv_extractor.extract()

# Transform
cleaner = DataCleaner()
data = cleaner.remove_nulls(data)
data = cleaner.standardize_columns(data)

aggregator = Aggregator()
data = aggregator.group_by(data, by=['region', 'product'], agg={'sales': 'sum'})

# Load
loader = DatabaseLoader(
    connection_string="postgresql://user:pass@localhost:5432/warehouse"
)
loader.load(data, table_name="sales_summary", if_exists="replace")

# Run pipeline
pipeline.run()
```


```python
# Run with config
from etl_pipeline import run_from_config

run_from_config("config.yaml")
```

## 🔧 Pipeline Components

### Extractors

| Extractor | Description | Usage |
|-----------|-------------|-------|
| `CSVExtractor` | Extract from CSV files | Local file system reads |
| `ExcelExtractor` | Extract from Excel files | Support for multiple sheets |
| `DatabaseExtractor` | Extract from SQL databases | Supports various RDBMS |
| `APIExtractor` | Extract from REST APIs | Handle pagination and auth |
| `S3Extractor` | Extract from AWS S3 | Cloud storage integration |

### Transformers

| Transformer | Description | Usage |
|-------------|-------------|-------|
| `DataCleaner` | Clean and validate data | Remove nulls, duplicates, outliers |
| `TypeConverter` | Convert data types | String to datetime, numeric conversion |
| `Aggregator` | Aggregate data | Group by, sum, average, count |
| `Joiner` | Merge datasets | Inner, outer, left, right joins |
| `FeatureEngineer` | Create new features | Calculate derived columns |
| `Validator` | Data quality checks | Schema validation, range checks |

### Loaders

| Loader | Description | Usage |
|--------|-------------|-------|
| `DatabaseLoader` | Load to SQL databases | Bulk insert, upsert operations |
| `CSVLoader` | Load to CSV files | Simple file output |
| `ParquetLoader` | Load to Parquet | Efficient columnar storage |
| `S3Loader` | Load to AWS S3 | Cloud storage upload |
| `DataWarehouseLoader` | Load to data warehouses | Optimized for Snowflake, Redshift |

## 📊 Data Quality & Validation

### Built-in Validation Rules

```python
from validators import DataValidator

validator = DataValidator()

# Schema validation
validator.validate_schema(data, expected_columns=['id', 'name', 'date', 'amount'])

# Data type validation
validator.validate_types(data, {
    'id': 'int64',
    'name': 'object',
    'date': 'datetime64',
    'amount': 'float64'
})

# Range validation
validator.validate_range(data, column='amount', min_value=0, max_value=1000000)

# Null check
validator.check_nulls(data, required_columns=['id', 'date'])

# Uniqueness check
validator.check_unique(data, columns=['id'])
```


## 👤 Author

**Ryan Heng**
- GitHub: [@ryanheng99](https://github.com/ryanheng99)
- Specialization: Data Engineering & ETL Pipeline Development

## 🙏 Acknowledgments

- Built for scalable data engineering workflows
- Designed with modularity and extensibility in mind
- Inspired by production-grade ETL best practices


