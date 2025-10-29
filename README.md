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

### Configuration File Approach

```python
# config.yaml
sources:
  - type: csv
    path: "data/input.csv"
  - type: database
    connection: "postgresql://localhost/sourcedb"
    query: "SELECT * FROM transactions WHERE date > '2024-01-01'"

transformations:
  - type: clean
    operations:
      - remove_duplicates
      - handle_nulls
  - type: aggregate
    group_by: ['customer_id', 'product_id']
    metrics:
      revenue: sum
      quantity: sum

destination:
  type: database
  connection: "postgresql://localhost/warehouse"
  table: "fact_sales"
  mode: append
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

## 📁 Project Structure

```
ETL_pipeline/
├── config/
│   ├── config.yaml             # Pipeline configurations
│   └── credentials.yaml        # Database credentials (gitignored)
├── src/
│   ├── extractors/
│   │   ├── __init__.py
│   │   ├── csv_extractor.py
│   │   ├── db_extractor.py
│   │   └── api_extractor.py
│   ├── transformers/
│   │   ├── __init__.py
│   │   ├── cleaner.py
│   │   ├── aggregator.py
│   │   └── validator.py
│   ├── loaders/
│   │   ├── __init__.py
│   │   ├── db_loader.py
│   │   └── file_loader.py
│   ├── utils/
│   │   ├── logger.py
│   │   ├── database.py
│   │   └── helpers.py
│   └── pipeline.py             # Main pipeline orchestration
├── data/
│   ├── raw/                    # Source data
│   ├── processed/              # Transformed data
│   └── archive/                # Historical loads
├── logs/                       # Execution logs
├── tests/
│   ├── test_extractors.py
│   ├── test_transformers.py
│   └── test_loaders.py
├── requirements.txt
├── .env.example
├── setup.py
└── README.md
```

## 🔐 Security Best Practices

### Credential Management

```python
# Use environment variables
import os
from dotenv import load_dotenv

load_dotenv()

db_config = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}
```

### .env.example Template

```bash
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=warehouse
DB_USER=etl_user
DB_PASSWORD=your_secure_password

# AWS Configuration
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1

# Pipeline Settings
LOG_LEVEL=INFO
BATCH_SIZE=10000
```

## 📈 Logging & Monitoring

### Logging Configuration

```python
import logging
from utils.logger import setup_logger

logger = setup_logger(
    name="etl_pipeline",
    log_file="logs/pipeline.log",
    level=logging.INFO
)

logger.info("Pipeline started")
logger.debug("Processing 10000 records")
logger.error("Failed to connect to database")
logger.warning("Data quality issue detected")
```

### Log Output Example

```
2024-10-29 10:15:23 - INFO - Pipeline started: sales_data_pipeline
2024-10-29 10:15:24 - INFO - Extracted 50000 records from CSV
2024-10-29 10:15:28 - INFO - Transformation complete: 49850 records
2024-10-29 10:15:28 - WARNING - 150 records removed due to validation
2024-10-29 10:15:35 - INFO - Loaded 49850 records to warehouse
2024-10-29 10:15:35 - INFO - Pipeline completed successfully
```

## ⚡ Performance Optimization

### Batch Processing

```python
# Process data in chunks for large datasets
from utils.batch_processor import BatchProcessor

processor = BatchProcessor(batch_size=10000)

for batch in processor.process_in_batches(large_dataframe):
    transformed_batch = transform(batch)
    load(transformed_batch)
```

### Parallel Processing

```python
from concurrent.futures import ThreadPoolExecutor

def process_file(file_path):
    data = extract(file_path)
    transformed = transform(data)
    load(transformed)

files = ['file1.csv', 'file2.csv', 'file3.csv']

with ThreadPoolExecutor(max_workers=4) as executor:
    executor.map(process_file, files)
```

## 🔄 Scheduling & Orchestration

### Cron Job Example

```bash
# Run daily at 2 AM
0 2 * * * cd /path/to/ETL_pipeline && /path/to/venv/bin/python src/pipeline.py
```

### Apache Airflow DAG

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def run_etl():
    from pipeline import ETLPipeline
    pipeline = ETLPipeline()
    pipeline.run()

dag = DAG(
    'etl_pipeline',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily'
)

etl_task = PythonOperator(
    task_id='run_etl',
    python_callable=run_etl,
    dag=dag
)
```

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_extractors.py
```

### Example Test

```python
import pytest
from extractors import CSVExtractor

def test_csv_extractor():
    extractor = CSVExtractor('tests/data/sample.csv')
    data = extractor.extract()
    
    assert len(data) > 0
    assert 'id' in data.columns
    assert data['id'].dtype == 'int64'
```

## 🤝 Contributing

We welcome contributions! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/NewExtractor`)
3. Write tests for your changes
4. Commit your changes (`git commit -m 'Add new S3 extractor'`)
5. Push to the branch (`git push origin feature/NewExtractor`)
6. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Write unit tests for all new features
- Update documentation for API changes
- Add type hints to function signatures
- Keep functions focused and modular

## 🐛 Troubleshooting

### Common Issues

**Database Connection Errors**
```python
# Check credentials and network access
# Verify firewall rules allow connections
# Test connection separately before pipeline run
```

**Memory Issues with Large Files**
```python
# Use chunking for large CSVs
chunksize = 10000
for chunk in pd.read_csv('large_file.csv', chunksize=chunksize):
    process(chunk)
```

**Data Type Mismatches**
```python
# Explicitly set dtypes during extraction
data = pd.read_csv('file.csv', dtype={'id': str, 'amount': float})
```

## 📚 Additional Resources

- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Apache Airflow](https://airflow.apache.org/)
- [Data Engineering Best Practices](https://www.getdbt.com/analytics-engineering/transformation/data-modeling-best-practices/)

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👤 Author

**Ryan Heng**
- GitHub: [@ryanheng99](https://github.com/ryanheng99)
- Specialization: Data Engineering & ETL Pipeline Development

## 🙏 Acknowledgments

- Built for scalable data engineering workflows
- Designed with modularity and extensibility in mind
- Inspired by production-grade ETL best practices

---

⭐ **If you find this useful, give it a star!**

📬 **Questions or suggestions?** Open an issue or contribute to the project!

💼 **Looking for enterprise support?** Reach out via GitHub for consulting opportunities.
