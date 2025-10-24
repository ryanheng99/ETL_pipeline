import pandas as pd
import xml.etree.ElementTree as ET
import os
import argparse
from collections import defaultdict
def convert_csv_to_xml(csv_file_path, data_source_name):
    # Load and clean the CSV
    df = pd.read_csv(csv_file_path)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df.dropna(how='all')

    # Organize data: Area → Unit → Tags
    structure = defaultdict(lambda: defaultdict(lambda: {'description': '', 'tags': []}))

    for _, row in df.iterrows():
        area = row['Area name']
        unit = row['Unit name']
        unit_desc = row['Unit description']
        tag = row['Tag name']
        tag_map = row['Tag map']
        alias_raw = str(row['Alias name']) if pd.notna(row['Alias name']) else ''

        structure[area][unit]['description'] = unit_desc

        # Check if tag already exists
        existing_tag = next((t for t in structure[area][unit]['tags'] if t['name'] == tag), None)

        if existing_tag:
            for alias in alias_raw.split(','):
                alias = alias.strip()
                if alias and alias not in existing_tag['aliases']:
                    existing_tag['aliases'].append(alias)
        else:
            aliases = [a.strip() for a in alias_raw.split(',') if a.strip()]
            structure[area][unit]['tags'].append({
                'name': tag,
                'map': tag_map,
                'dataSourceName': data_source_name,
                'aliases': aliases
            })

    # Build XML tree
    root = ET.Element('Definition', xmlns='SYSTEM_NAMESPACE')

    for area, units in structure.items():
        area_elem = ET.SubElement(root, 'Area', name=area)
        unit_defs = ET.SubElement(area_elem, 'UnitDefinitions')

        for unit, unit_data in units.items():
            unit_elem = ET.SubElement(unit_defs, 'UnitDefinition',
                                      name=unit,
                                      description=unit_data['description'],
                                      type='')  # Optional: define type if needed
            tag_defs = ET.SubElement(unit_elem, 'TagDefinitions')

            for tag in unit_data['tags']:
                tag_elem = ET.SubElement(tag_defs, 'TagDefinition',
                                         name=tag['name'],
                                         map=tag['map'],
                                         dataSourceName=tag['dataSourceName'])
                alias_defs = ET.SubElement(tag_elem, 'AliasDefinitions')

                for alias in tag['aliases']:
                    ET.SubElement(alias_defs, 'AliasDefinition', name=alias)

    ET.indent(root, space='    ')
    output_file = f"{os.path.splitext(csv_file_path)[0]}_{data_source_name}.xml"
    ET.ElementTree(root).write(output_file, encoding='utf-8', xml_declaration=False)
    print(f"XML file created: {output_file}")

def validate_aliases(df):
    # Basic validation: check for duplicate aliases per unit
    test_ok = True
    alias_check = df.groupby(['Area name', 'Unit name'])['Alias name'].nunique()
    if any(alias_check < df.groupby(['Area name', 'Unit name'])['Alias name'].count()):
        print("Warning: Duplicate alias names detected. Please review your CSV.")
        test_ok = False
    return test_ok

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert structured CSV to XML format.')
    parser.add_argument('-d', '--datasource', required=True,
                        help='Data source name (e.g., "DATA_SOURCE_NAME")')
    parser.add_argument('csv_file', nargs='?', help='Path to CSV file')

    args = parser.parse_args()
    data_source_name = args.datasource

    files_to_process = []

    if args.csv_file:
        if os.path.exists(args.csv_file) and args.csv_file.endswith('.csv'):
            files_to_process.append(args.csv_file)
        else:
            print("Invalid file path or format.")
            exit(1)
    else:
        files_to_process = [f for f in os.listdir('.') if f.endswith('.csv')]

    for csv_file_path in files_to_process:
        df = pd.read_csv(csv_file_path)
        if validate_aliases(df):
            convert_csv_to_xml(csv_file_path, data_source_name)
        else:
            print(f"Skipping file due to validation issues: {csv_file_path}")

            