import geopandas as gpd
import os
from pathlib import Path


def get_all_municipalities():
    print("=== Spanish Census Municipalities Processing ===")
    print("Processing INE districts into municipalities...\n")
    script_dir = Path(__file__).parent
    data_path = script_dir / "../data/processed/distritos_2025.geojson"
    output_path = script_dir / "../data/processed/municipios_2025.geojson"

    # Create processed directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

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
        print("   Make sure to run scripts/get_all_districts.py first to create the distritcs file.")
        return

    print("\n2. Analyzing available fields...")
    available_fields = list(gdf.columns)
    print(f"   Available fields: {available_fields}")

    print("\n3. Grouping by municipality and dissolving geometries...")
    try:
        # Group by province and municipality
        municipalities_gdf = gdf.dissolve(
            by=['CUMUN'],
            as_index=False
        )
        print(
            f"   ✓ Created {len(municipalities_gdf)} municipalities from {len(gdf)} districts")
    except Exception as e:
        print(f"ERROR during dissolve: {e}")
        return

    print("\n4. Selecting fields to keep...")
    # Define fields to keep (district level and above)
    fields_to_keep = [
        "CUMUN", "CMUN", "NMUN",  # Municipality level
        "CPRO", "NPRO",  # Province level
        "CCA", "NCA",  # Community level
        "geometry"
    ]

    # Keep only fields that exist in the data
    final_fields = [
        field for field in fields_to_keep if field in municipalities_gdf.columns]
    excluded_fields = [
        field for field in municipalities_gdf.columns if field not in final_fields]

    print(f"   Fields to keep: {final_fields}")
    print(f"   Fields excluded: {excluded_fields}")

    # Apply field selection
    filtered_gdf = municipalities_gdf[final_fields]

    print("\n6. Exporting to GeoJSON...")
    try:
        filtered_gdf.to_file(str(output_path), driver="GeoJSON")
        print(f"   ✓ Successfully exported to {output_path}")
    except Exception as e:
        print(f"ERROR during export: {e}")
        return

    print("\n=== Processing Summary ===")
    print(f"Input districts: {len(gdf)}")
    print(f"Output municipalities: {len(filtered_gdf)}")
    print(f"Fields in output: {len(final_fields)}")
    print(
        f"Output file size: {os.path.getsize(output_path) / 1024 / 1024:.2f} MB")

    print("\n✓ Processing completed successfully!")
    print(f"Municipalities GeoJSON saved to: {output_path}")


if __name__ == "__main__":
    get_all_municipalities()
