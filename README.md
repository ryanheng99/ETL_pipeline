Overview

This repository contains two data pipelines designed for manufacturing data processing and analysis. Pipeline 1 performs ETL operations to create an engineering master table by integrating multiple data sources and calculating time-based statistics.
Pipeline 1: Manufacturing Data ETL Pipeline
Purpose
Pipeline 1 consolidates manufacturing testing data, APRM batch records, and DCS operational data into a unified master table for engineering analysis. It calculates statistical metrics (average, standard deviation, max, min) for process parameters across different event windows within each batch.
Input Data Sources
FileDescriptionKey ColumnsProcessed_TestingMFGData.csvTime-series process dataTime, Parameter 1, Parameter 2, Parameter 3APRM_data.csvBatch event timestampsBatch_ID, E1_start, E1_end, E2_start, E2_end, E3_start, E3_endDCS_data.xlsxDCS operational dataTime, valve_position, pump_speed
Output
File: Master_table.csv
Structure: One row per batch with the following columns:

Batch_ID - Unique batch identifier
For each event (E1, E2, E3):

E{n}_start, E{n}_end - Event time boundaries
E{n}_ValvePosAtStart - Numeric valve position (0=Close, 1=Open)
E{n}_ValveStatusAtStart - Text valve status (Open/Close/Partial/Unknown)
E{n}_AvgPumpSpd - Average pump speed (RPM) over the event duration
E{n}_AvgPara{1,2,3} - Average parameter values
E{n}_SDPara{1,2,3} - Standard deviation of parameters
E{n}_MaxPara{1,2,3} - Maximum parameter values
E{n}_MinPara{1,2,3} - Minimum parameter values



Key Features

Time-Range Based Calculations: All statistics are calculated for exact time windows defined by event start/end times
DCS Data Integration: Captures valve positions and averages pump speeds over event durations
Multi-Parameter Statistics: Computes comprehensive statistics for 3 process parameters
Data Type Preservation: Maintains appropriate data types (float for numeric, object for IDs/timestamps)
Robust Error Handling: Gracefully handles missing data and edge cases

Prerequisites
bashPython 3.7+
pandas
numpy
openpyxl  # For Excel file reading
Installation
bashpip install pandas numpy openpyxl
Usage

Place input files in the same directory as the script:

Processed_TestingMFGData.csv
APRM_data.csv
DCS_data.xlsx


Run the pipeline:

bash   python pipeline1.py

Output will be generated:

Master_table.csv - Consolidated master table



Process Flow
┌─────────────────────────────────────────────────────────────┐
│                         EXTRACT                             │
├─────────────────────────────────────────────────────────────┤
│  Load Source Data (CSV) → Time-series process parameters    │
│  Load APRM Data (CSV)   → Batch event timestamps           │
│  Load DCS Data (XLSX)   → Valve & pump operational data    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                       TRANSFORM                             │
├─────────────────────────────────────────────────────────────┤
│  For each Batch:                                            │
│    For each Event (E1, E2, E3):                            │
│      1. Filter DCS data by time range                      │
│         → Get valve position at start                      │
│         → Calculate average pump speed                     │
│      2. Filter source data by time range                   │
│         → Calculate parameter statistics                   │
│           (Avg, SD, Max, Min for Para1, Para2, Para3)     │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                          LOAD                               │
├─────────────────────────────────────────────────────────────┤
│  Save consolidated master table to CSV                      │
│  Display data type summary and sample output               │
└─────────────────────────────────────────────────────────────┘
Functions
FunctionPurposeload_csv_files()Loads all input data files with proper data type handlingconvert_valve_position_to_text()Converts numeric valve positions to readable statusget_dcs_data_for_timerange()Extracts DCS data for specific time windowscalculate_parameter_stats_for_timerange()Computes statistics for parameters within time rangescreate_master_table()Main transformation logic - builds consolidated tablesave_master_table()Saves output and displays summary statisticsmain()Orchestrates the complete ETL process
Logging
The pipeline provides detailed console logging including:

File loading status and record counts
Processing progress for each batch and event
Data availability warnings
Calculated statistics preview
Final output summary with data types

Error Handling

Missing input files: Process terminates with error message
Missing time ranges: Populates with NaN values
No data in time range: Logs warning and continues
Invalid numeric values: Converts to NaN using pandas errors='coerce'

Pipeline 2: CSV to XML Configuration Converter
Purpose
Pipeline 2 converts structured CSV tag configuration files into hierarchical XML format for system integration. It organizes industrial tags by Area → Unit → Tag structure with alias management and data source mapping.
Input Data Source
File Format: CSV file with the following columns:
ColumnDescriptionArea nameProcess area identifierUnit nameUnit/equipment identifier within areaUnit descriptionDescription of the unitTag nameUnique tag identifierTag mapTag mapping referenceAlias nameComma-separated list of tag aliases
Example Input:
csvArea name,Unit name,Unit description,Tag name,Tag map,Alias name
Area1,Unit101,Primary Reactor,TEMP_01,T-101,Temperature1,Temp_Reactor
Area1,Unit101,Primary Reactor,PRES_01,P-101,Pressure1
Area2,Unit202,Secondary Tank,LEVEL_01,L-202,Level1,Tank_Level
Output
File: {input_filename}_{datasource}.xml
Structure: Hierarchical XML with namespace definition
xml<Definition xmlns="SYSTEM_NAMESPACE">
  <Area name="Area1">
    <UnitDefinitions>
      <UnitDefinition name="Unit101" description="Primary Reactor" type="">
        <TagDefinitions>
          <TagDefinition name="TEMP_01" map="T-101" dataSourceName="DATA_SOURCE_NAME">
            <AliasDefinitions>
              <AliasDefinition name="Temperature1"/>
              <AliasDefinition name="Temp_Reactor"/>
            </AliasDefinitions>
          </TagDefinition>
        </TagDefinitions>
      </UnitDefinition>
    </UnitDefinitions>
  </Area>
</Definition>
Key Features

Hierarchical Structure: Automatically organizes tags into Area → Unit → Tag hierarchy
Alias Consolidation: Merges multiple aliases for the same tag from comma-separated values
Duplicate Prevention: Detects and consolidates duplicate tag entries
Batch Processing: Can process single file or all CSV files in directory
Data Validation: Validates aliases before conversion
Clean Output: Removes unnamed columns and empty rows

Prerequisites
bashPython 3.7+
pandas
Installation
bashpip install pandas
Usage
Process a single CSV file:
bashpython pipeline2.py -d DATA_SOURCE_NAME input_tags.csv
Process all CSV files in current directory:
bashpython pipeline2.py -d DATA_SOURCE_NAME
Arguments:

-d, --datasource (required): Data source name to be embedded in XML
csv_file (optional): Specific CSV file to process. If omitted, processes all CSV files in directory

Process Flow
┌─────────────────────────────────────────────────────────────┐
│                      INPUT VALIDATION                       │
├─────────────────────────────────────────────────────────────┤
│  • Check file exists and is CSV format                      │
│  • Validate alias uniqueness per unit                       │
│  • Remove unnamed columns and empty rows                    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    DATA STRUCTURING                         │
├─────────────────────────────────────────────────────────────┤
│  Build nested structure:                                    │
│    Area → Unit → Tags                                       │
│  • Group tags by Area and Unit                             │
│  • Parse comma-separated aliases                           │
│  • Consolidate duplicate tags                              │
│  • Preserve unit descriptions                              │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                     XML GENERATION                          │
├─────────────────────────────────────────────────────────────┤
│  • Create hierarchical XML structure                        │
│  • Add namespace declaration                                │
│  • Format with proper indentation (4 spaces)               │
│  • Write to output file                                     │
└─────────────────────────────────────────────────────────────┘
Functions
FunctionPurposeconvert_csv_to_xml()Main conversion logic - transforms CSV to hierarchical XMLvalidate_aliases()Validates alias uniqueness within each unitCommand-line parserHandles arguments for datasource and file selection
Data Quality Rules
Duplicate Handling:

If the same tag appears multiple times in a unit, aliases are merged
Duplicate aliases for the same tag are automatically removed

Cleaning Operations:

Removes columns with names starting with "Unnamed"
Drops rows that are completely empty
Strips whitespace from alias names
Handles missing alias values gracefully

Validation
The pipeline performs validation before conversion:
Alias Validation:

Checks for duplicate alias names within the same unit
Warns if validation issues are detected
Skips file processing if critical validation fails

Example warning:
Warning: Duplicate alias names detected. Please review your CSV.
Skipping file due to validation issues: input_tags.csv
Example Workflow
Input CSV:
csvArea name,Unit name,Unit description,Tag name,Tag map,Alias name
Plant_A,Reactor_01,Main Reactor,TEMP_HIGH,TH-001,HighTemp,ReactorTemp
Plant_A,Reactor_01,Main Reactor,TEMP_HIGH,TH-001,OverTemp
Plant_A,Reactor_01,Main Reactor,PRES_LOW,PL-001,LowPressure
Command:
bashpython pipeline2.py -d SCADA_SYSTEM input_tags.csv
Output: input_tags_SCADA_SYSTEM.xml
The tag TEMP_HIGH will have three aliases consolidated: HighTemp, ReactorTemp, and OverTemp.

Troubleshooting
Common Issues
Issue: FileNotFoundError

Solution: Ensure all input files are in the same directory as the script

Issue: No DCS data found for time range

Solution: Check that DCS data timestamps overlap with APRM event times

Issue: Column not found errors

Solution: Verify column names in input files match expected format (e.g., "Parameter 1" with space)

Issue: Excel file read errors

Solution: Install openpyxl: pip install openpyxl

Data Quality Checks
Before running the pipeline, verify:

Time columns are in consistent datetime format
APRM event times are sequential (start < end)
No duplicate Batch_IDs in APRM data
Numeric columns contain valid values


Contributing
When modifying the pipeline:

Maintain backward compatibility with existing output format
Add comprehensive error handling for new features
Update logging to track new operations
Test with edge cases (missing data, boundary times)
