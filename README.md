# ETL-Pipeline-1
ETL Master Data Pipeline
Overview
This project implements Data Pipeline 1, an ETL (Extract, Transform, Load) workflow designed to consolidate master data from multiple manufacturing systems—primarily APRM, DCS, and optionally MES, LIMS, and others—into a unified, validated master table. The pipeline supports scalable integration, robust transformation logic, and downstream analytics enablement.
Objectives

Unify disparate data sources into a single master table.
Standardize and validate incoming data formats.
Enable traceability across systems for manufacturing analytics.
Support modular extension for future data sources.

Architecture:
| APRM Source  | --> |                | --> |                | --> |                              |
| DCS Source   | --> | Extraction     | --> | Transformation | --> | Unified Table (Master Table) |
| MFGData      | --> |                | --> |                | --> |                              |


Data Sources

Historian: APRM – Equipment and recipe data (e.g., setpoints, control parameters, batch configurations)
DCS: Real-time process data – Temperature, pressure, flow rates, sensor readings

Technologies Used

Python: Core ETL logic
SQL: Data extraction and transformation
Pandas: Data manipulation



