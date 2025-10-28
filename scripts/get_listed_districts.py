import geopandas as gpd
import os
from pathlib import Path
from datetime import datetime


def main(cumun_to_extract):
    print("=== Spanish Census Districts Processing ===")
    print("Getting Specified Municipalities...\n")

    # Set up paths
    script_dir = Path(__file__).parent
    data_path = script_dir / "../data/processed/distritos_2025.geojson"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = script_dir / \
        f"../output/filtered_districts_2025_{timestamp}.geojson"

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

    # Show available fields
    print("\n2. Analyzing available fields...")
    available_fields = list(gdf.columns)
    print(f"   Available fields: {available_fields}")

    print("\n3. Getting listed Municipalities")
    filtered_gdf = gdf[gdf["CUMUN"].isin(cumun_to_extract)]

    print(f"Matched {len(filtered_gdf)} of {len(gdf)} rows")

    # Check for missing municipality codes
    found_codes = set(filtered_gdf["CUMUN"].unique())
    missing_codes = set(cumun_to_extract) - found_codes
    if missing_codes:
        print(f"\n❌ Missing municipality codes not found in data:")
        for missing in sorted(missing_codes):
            print(f"   ❌ {missing}")
    else:
        print(f"\n✓ All {len(cumun_to_extract)} municipality codes found in data")

    print("\n4. Exporting to GeoJSON...")
    try:
        filtered_gdf.to_file(str(output_path), driver="GeoJSON")
        print(f"   ✓ Successfully exported to {output_path}")
    except Exception as e:
        print(f"ERROR during export: {e}")
        return

    print("\n=== Processing Summary ===")
    print(f"Input sections: {len(gdf)}")
    print(f"Output districts: {len(filtered_gdf)}")
    print(f"Municipalities: {len(cumun_to_extract)}")
    print(
        f"Output file size: {os.path.getsize(output_path) / 1024 / 1024:.2f} MB")

    print("\n✓ Processing completed successfully!")
    print(f"Districts GeoJSON saved to: {output_path}")


if __name__ == "__main__":
    cumun_to_extract = [
        "01059", "08015", "08019", "08096", "08113", "08121",
        "08124", "08205", "08211", "08245", "08301", "08307",
        "20069", "28079", "30027", "46220", "46250", "50297"
    ]
    main(cumun_to_extract)
