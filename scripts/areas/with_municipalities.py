import geopandas as gpd
import os
from pathlib import Path


def area_with_municipalities(area_name, area):
    print("=== Spanish Area Processing ===")
    print(f"Getting {area_name} municipalities...\n")

    script_dir = Path(__file__).parent
    data_path = script_dir / f"../../output/{area_name}/{area_name}_with_districts.geojson"
    output_path = script_dir / \
        f"../../output/{area_name}/{area_name}_with_municipalities.geojson"

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
    # Check for missing municipalities
    found_municipalities = set(filtered_gdf["NMUN"].unique())
    missing_municipalities = set(area) - found_municipalities
    if missing_municipalities:
        print(f"\n❌ Missing municipalities not found in data:")
        for missing in sorted(missing_municipalities):
            print(f"   ❌ {missing}")
    else:
        print(f"\n✓ All {len(area)} municipalities found in data")

    print("\n4. Grouping by municipality")
    try:
        temp_gdf = filtered_gdf
        temp_gdf = filtered_gdf.dissolve(by=['CMUN'], as_index=False)
        
        print(
            f"   ✓ Created {len(temp_gdf)} districts from {len(filtered_gdf)} sections")
        filtered_gdf = temp_gdf
    except Exception as e:
        print(f"ERROR during dissolve: {e}")
        return
    
    

    print("\n5. Selecting fields to keep...")
    fields_to_keep = [
        "CUMUN", "CMUN", "NMUN",  # Municipality level
        "CPRO", "NPRO",  # Province level
        "CCA", "NCA",  # Community level
        "geometry"
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
    print(f"Output districts: {len(filtered_gdf)}")
    print(f"Municipalities: {len(area)}")
    print(
        f"Output file size: {os.path.getsize(output_path) / 1024 / 1024:.2f} MB")

    print("\n✓ Processing completed successfully!")
    print(f"Districts GeoJSON saved to: {output_path}")
