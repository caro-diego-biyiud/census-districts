import geopandas as gpd
import pandas as pd
import os
from pathlib import Path


def total_area(csv_path):
    print("=== Spanish Area Processing ===")

    # Read CSV and extract area name
    csv_path = Path(csv_path)
    area_name = csv_path.stem
    print(f"Getting {area_name} municipalities...\n")

    # Read area definition from CSV
    try:
        area_df = pd.read_csv(csv_path, delimiter=';', encoding='utf-8')
        print(f"   ✓ Loaded area definition with {len(area_df)} entries")
        print(f"   ✓ Fields: {area_df['field'].unique().tolist()}")
    except Exception as e:
        print(f"ERROR reading CSV file: {e}")
        return

    script_dir = Path(__file__).parent
    data_path = script_dir / f"../../output/areas/{area_name}/{area_name}_with_municipalities.geojson"
    output_path = script_dir / \
        f"../../output/areas/{area_name}/{area_name}_only_area.geojson"

    print(f"Input file: {data_path}")
    print(f"Output file: {output_path}")

    # Check if input file exists
    if not data_path.exists():
        print(f"ERROR: Input file not found at {data_path}")
        return

    print("\n1. Loading GeoJSON...")
    try:
        gdf = gpd.read_file(str(data_path))
        print(f"   ✓ Loaded {len(gdf)} census sections")
        print(f"   ✓ CRS: {gdf.crs}")
    except Exception as e:
        print(f"ERROR loading GeoJSON: {e}")
        print("   Make sure to run scripts/convert_to_geojson.py first to create the interim file.")
        return

    print("\n2. Analyzing available fields...")
    available_fields = list(gdf.columns)
    print(f"   Available fields: {available_fields}")


    filtered_gdf = gdf

    # Check for missing values by field (only for fields that exist in data)
    print("\n3. Validating CSV criteria against data")
    for field, group in area_df.groupby('field'):
        if field in gdf.columns:
            values = set(group['value'].tolist())
            found_values = set(gdf[field].unique())
            missing_values = values - found_values
            if missing_values:
                print(f"   ❌ Missing {field} values not found in data:")
                for missing in sorted(missing_values):
                    print(f"      ❌ {missing}")
            else:
                print(f"   ✓ All {len(values)} {field} values found in data")
        else:
            print(f"   ⚠️  Field '{field}' not found in data columns: {list(gdf.columns)}")

    print("\n4. Grouping by area")
    try:
        temp_gdf = filtered_gdf
        # temp_gdf = filtered_gdf.dissolve(by=['CCA'], as_index=False)
        temp_gdf = filtered_gdf.dissolve()

        # Add area name field to the dissolved geometry
        temp_gdf['area_name'] = area_name

        print(
            f"   ✓ Created {len(temp_gdf)} area from {len(filtered_gdf)} municipalities")
        filtered_gdf = temp_gdf
    except Exception as e:
        print(f"ERROR during dissolve: {e}")
        return
    
    

    print("\n5. Selecting fields to keep...")
    fields_to_keep = [
        "geometry",
        "area_name"
    ]

    # Keep only fields that exist in the data
    final_fields = [
        field for field in fields_to_keep if field in filtered_gdf.columns]
    excluded_fields = [
        field for field in filtered_gdf.columns if field not in final_fields]

    print(f"   Fields to keep: {final_fields}")
    print(f"   Fields excluded: {excluded_fields}")

    filtered_gdf = filtered_gdf[final_fields]

    print("\n6. Exporting to GeoJSON")
    # Create output directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        filtered_gdf.to_file(str(output_path), driver="GeoJSON")
        print(f"   ✓ Successfully exported to {output_path}")
    except Exception as e:
        print(f"ERROR during export: {e}")
        return

    print("\n=== Processing Summary ===")
    print(f"Input sections: {len(gdf)}")
    print(f"Output area: {len(filtered_gdf)}")
    print(f"CSV entries: {len(area_df)}")
    print(f"CSV fields: {area_df['field'].unique().tolist()}")
    print(
        f"Output file size: {os.path.getsize(output_path) / 1024 / 1024:.2f} MB")

    print("\n✓ Processing completed successfully!")
    print(f"Area GeoJSON saved to: {output_path}")
