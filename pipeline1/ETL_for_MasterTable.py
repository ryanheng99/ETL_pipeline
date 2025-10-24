import pandas as pd
import numpy as np

def load_csv_files():
    print("Loading CSV files with specified data types...")
    
    try:
        # Load source data - time(object), parameter_1(float), parameter_2(float), parameter_3(float)
        print("Loading source_data.csv...\n")
        source_data = pd.read_csv("Processed_TestingMFGData.csv") 
        source_data['Time'] = pd.to_datetime(source_data['Time'])
        
        # Load APRM data - all columns as object (no datetime conversion)
        print("Loading aprm_data.csv...\n")
        aprm_data = pd.read_csv("APRM_data.csv", dtype=str)  # Keep all as strings/objects
        
        # Load DCS data - Time(object), valve_position(float), pump_speed(float)
        print("Loading dcs_data.csv...\n")
        dcs_data = pd.read_excel("DCS_data.xlsx")

        # Keep Time as object, but create a datetime version for filtering
        dcs_data['Time_dt'] = pd.to_datetime(dcs_data['Time'])
        
        print("All files loaded successfully\n")
        print(f"   Source data: {len(source_data)} records")
        print(f"   APRM data: {len(aprm_data)} batches")
        print(f"   DCS data: {len(dcs_data)} records")
        
        return source_data, aprm_data, dcs_data
        
    except Exception as e:
        print(f"Error loading files: {e}")
        return None, None, None

def convert_valve_position_to_text(valve_position):
    # Convert numeric valve position to text representation
    if pd.isna(valve_position):
        return "Unknown"
    elif valve_position == 1:
        return "Open"
    elif valve_position == 0:
        return "Close"
    else:
        # Handle intermediate positions (if any)
        return f"Partial ({valve_position})"

def get_dcs_data_for_timerange(dcs_data, start_time_str, end_time_str):
    
    try:
        # Convert string times to datetime for comparison
        start_time = pd.to_datetime(start_time_str)
        end_time = pd.to_datetime(end_time_str)
        
        # Filter DCS data within the exact time range using datetime version
        dcs_subset = dcs_data[
            (dcs_data['Time_dt'] >= start_time) & 
            (dcs_data['Time_dt'] <= end_time)
        ]
        
        if len(dcs_subset) == 0:
            print(f"No DCS data found for range {start_time} to {end_time}")
            return np.nan, np.nan
        
        print(f"DCS data found: {len(dcs_subset)} records in range")
        
        # Take the first valve position value (valve position doesn't change frequently)
        valve_position = dcs_subset['valve_position'].iloc[0]
        
        # Calculate AVERAGE pump speed over the entire time range
        pump_speed_data = pd.to_numeric(dcs_subset['pump_speed'], errors='coerce').dropna()
        
        if len(pump_speed_data) > 0:
            avg_pump_speed = float(pump_speed_data.mean())
            print(f"Calculated average pump speed: {avg_pump_speed:.2f} from {len(pump_speed_data)} records")
        else:
            avg_pump_speed = np.nan
            print("No valid pump speed data found")
        
        return float(valve_position), avg_pump_speed
        
    except Exception as e:
        print(f"Error getting DCS data: {e}")
        return np.nan, np.nan

def calculate_parameter_stats_for_timerange(source_data, start_time_str, end_time_str, event_name):
    # Calculate parameter statistics for a specific time range
    
    try:
        print(f"Calculating stats for {event_name}: {start_time_str} to {end_time_str}")
        
        # Convert string times to datetime for comparison
        start_time = pd.to_datetime(start_time_str)
        end_time = pd.to_datetime(end_time_str)
        
        # Filter source data within the exact time range (note: column is 'Time', not 'time')
        time_subset = source_data[
            (source_data['Time'] >= start_time) & 
            (source_data['Time'] <= end_time)
        ]
        
        if len(time_subset) == 0:
            print(f"No source data found for {event_name} time range\n")
            return {f'para{i}_{stat}': np.nan for i in [1,2,3] for stat in ['avg','sd','max','min']}
        
        print(f"Found {len(time_subset)} records for {event_name}")
        
        stats = {}
        
        # Calculate stats for each parameter within the time range
        # Check what parameter columns actually exist in the source data
        available_columns = time_subset.columns.tolist()
        print(f"Available columns in source data: {available_columns}\n")
        
        for param_num in [1, 2, 3]:
            # Use the exact column names with spaces
            param_col = f'Parameter {param_num}'
            
            if param_col in time_subset.columns:
                print(f"Found parameter column: {param_col}\n")
                # Get parameter data and convert to numeric
                param_data = pd.to_numeric(time_subset[param_col], errors='coerce').dropna()
                
                if len(param_data) > 0:
                    stats[f'para{param_num}_avg'] = float(param_data.mean())
                    stats[f'para{param_num}_sd'] = float(param_data.std()) if len(param_data) > 1 else 0.0
                    stats[f'para{param_num}_max'] = float(param_data.max())
                    stats[f'para{param_num}_min'] = float(param_data.min())
                    print(f"Calculated stats for {param_col}: avg={stats[f'para{param_num}_avg']:.2f}\n")
                else:
                    stats[f'para{param_num}_avg'] = np.nan
                    stats[f'para{param_num}_sd'] = np.nan
                    stats[f'para{param_num}_max'] = np.nan
                    stats[f'para{param_num}_min'] = np.nan
            else:
                print(f"Column '{param_col}' not found in source data\n")
                stats[f'para{param_num}_avg'] = np.nan
                stats[f'para{param_num}_sd'] = np.nan
                stats[f'para{param_num}_max'] = np.nan
                stats[f'para{param_num}_min'] = np.nan
        
        return stats
        
    except Exception as e:
        print(f"Error calculating parameter stats: {e}\n")
        return {f'para{i}_{stat}': np.nan for i in [1,2,3] for stat in ['avg','sd','max','min']}

def create_master_table(source_data, aprm_data, dcs_data):
    # Create master table with proper data types for engineering analysis
    print("\nGenerating Engineering Master Table...\n")
    
    master_records = []
    
    # Process each batch
    for batch_idx, batch_row in aprm_data.iterrows():
        batch_id = str(batch_row['Batch_ID'])  # Keep as object (string)
        print(f"\nProcessing {batch_id}...\n")
        
        # Initialize master record
        master_record = {'Batch_ID': batch_id}
        
        # Process each event (E1, E2, E3)
        for event_num in [1, 2, 3]:
            start_col = f'E{event_num}_start'
            end_col = f'E{event_num}_end'
            
            print(f"Processing Event {event_num}...\n")
            
            if start_col in batch_row.index and end_col in batch_row.index:
                start_time_str = batch_row[start_col]  # Keep as string/object
                end_time_str = batch_row[end_col]      # Keep as string/object
                
                # Add start and end times as objects (keep original strings)
                master_record[start_col] = start_time_str if pd.notna(start_time_str) else None
                master_record[end_col] = end_time_str if pd.notna(end_time_str) else None
                
                # Skip processing if times are missing or empty
                if pd.isna(start_time_str) or pd.isna(end_time_str) or start_time_str == '' or end_time_str == '':
                    print(f"Missing times for Event {event_num}")
                    # Fill with NaN values
                    master_record[f'E{event_num}_ValvePosAtStart'] = np.nan
                    master_record[f'E{event_num}_ValveStatusAtStart'] = "Unknown"
                    master_record[f'E{event_num}_AvgPumpSpd'] = np.nan  # Changed from PumpSpd to AvgPumpSpd
                    for param_num in [1, 2, 3]:
                        master_record[f'E{event_num}_AvgPara{param_num}'] = np.nan
                        master_record[f'E{event_num}_SDPara{param_num}'] = np.nan
                        master_record[f'E{event_num}_MaxPara{param_num}'] = np.nan
                        master_record[f'E{event_num}_MinPara{param_num}'] = np.nan
                    continue
                
                # Get DCS data for this exact time range (pass strings)
                valve_pos, avg_pump_speed = get_dcs_data_for_timerange(dcs_data, start_time_str, end_time_str)
                master_record[f'E{event_num}_ValvePosAtStart'] = valve_pos  # float (original numeric value)
                master_record[f'E{event_num}_ValveStatusAtStart'] = convert_valve_position_to_text(valve_pos)  # text representation
                master_record[f'E{event_num}_AvgPumpSpd'] = avg_pump_speed  # float - AVERAGE pump speed over time range
                
                # Get parameter statistics for this exact time range (pass strings)
                param_stats = calculate_parameter_stats_for_timerange(
                    source_data, start_time_str, end_time_str, f"E{event_num}"
                )
                
                # Add parameter stats with proper float data types
                for param_num in [1, 2, 3]:
                    master_record[f'E{event_num}_AvgPara{param_num}'] = param_stats[f'para{param_num}_avg']  # float
                    master_record[f'E{event_num}_SDPara{param_num}'] = param_stats[f'para{param_num}_sd']   # float
                    master_record[f'E{event_num}_MaxPara{param_num}'] = param_stats[f'para{param_num}_max'] # float
                    master_record[f'E{event_num}_MinPara{param_num}'] = param_stats[f'para{param_num}_min'] # float
            
            else:
                print(f"Event {event_num} columns not found")
        
        master_records.append(master_record)
        print(f"{batch_id} processed successfully")
    
    # Create DataFrame
    master_table = pd.DataFrame(master_records)
    
    print(f"\nMaster table created with {len(master_table)} batches")
    return master_table

def save_master_table(master_table):
    # """Save master table with proper data types"""
    print("\nSaving master table...")
    
    # Save to CSV
    master_table.to_csv("Master_table.csv", index=False)
    
    print("Master table saved as 'Master_table.csv'")
    print(f"Total batches: {len(master_table)}")
    print(f"Total columns: {len(master_table.columns)}")
    
    # Show data types
    print(f"\nData Types Summary:")
    dtype_summary = master_table.dtypes.value_counts()
    for dtype, count in dtype_summary.items():
        print(f"  {dtype}: {count} columns")
    
    # Show sample of first batch
    print(f"\nSample - First Batch Data:")
    if len(master_table) > 0:
        first_batch = master_table.iloc[0]
        print(f"  Batch ID: {first_batch['Batch_ID']}")
        
        for event_num in [1, 2, 3]:
            if f'E{event_num}_start' in first_batch.index:
                print(f"  E{event_num}: {first_batch[f'E{event_num}_start']} to {first_batch[f'E{event_num}_end']}")
                valve_status = first_batch[f'E{event_num}_ValveStatusAtStart'] if f'E{event_num}_ValveStatusAtStart' in first_batch.index else "N/A"
                # Updated to show AvgPumpSpd instead of PumpSpd
                print(f"      Valve: {first_batch[f'E{event_num}_ValvePosAtStart']:.2f} ({valve_status}), Avg Pump: {first_batch[f'E{event_num}_AvgPumpSpd']:.1f} RPM")
                print(f"      Para1 Avg: {first_batch[f'E{event_num}_AvgPara1']:.2f}, SD: {first_batch[f'E{event_num}_SDPara1']:.2f}")

def main():
    # Main ETL function for engineering analysis
    print("ETL Process Starts...")
    
    try:
        # Extract: Load all CSV files with proper data types
        source_data, aprm_data, dcs_data = load_csv_files()
        
        if source_data is None:
            print("Failed to load data files")
            return
        
        # Transform: Create master table with time-range based calculations
        master_table = create_master_table(source_data, aprm_data, dcs_data)
        
        # Load: Save master table
        save_master_table(master_table)
        
        print("\nETL Process completed successfully!")
        print("Output file: Master_table.csv")
        
    except Exception as e:
        print(f"Process failed: {e}")

if __name__ == "__main__":
    main()
