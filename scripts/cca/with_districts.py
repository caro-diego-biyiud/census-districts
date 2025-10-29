import geopandas as gpd
import pandas as pd
import os
from pathlib import Path

def cca_with_districts(cca):
    print("=== Autonomous Community Processing ===")

    script_dir = Path(__file__).parent
    data_path = script_dir / "../../data/processed/distritos_2025.geojson"
    output_path = script_dir / \
        f"../../output/CCA/CCA_{cca}/{cca}_with_districts.geojson"

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

    print(f"\n3. Filtering districts for CCA {cca}...")
    filtered_gdf = gdf[gdf["CCA"] == cca]
    print(
        f"   ✓ Filtered to {len(filtered_gdf)} districts from {len(gdf)} total")

    if len(filtered_gdf) == 0:
        print(f"   ❌ No districts found for CCA {cca}")
        available_ccas = sorted(gdf["CCA"].unique())
        print(f"   Available CCAs: {available_ccas}")
        return

    print(f"   ✓ Total matched: {len(filtered_gdf)} of {len(gdf)} rows")

    print("\n4. Selecting fields to keep...")
    fields_to_keep = [
        "CUDIS", "CDIS",  # District level
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

    print("\n5. Exporting to GeoJSON")
    # Create output directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        filtered_gdf.to_file(str(output_path), driver="GeoJSON")
        print(f"   ✓ Successfully exported to {output_path}")
    except Exception as e:
        print(f"ERROR during export: {e}")
        return


    print("\n=== Processing Summary ===")
    print(f"Input districts: {len(gdf)}")
    print(f"Output districts: {len(filtered_gdf)}")
    print(
        f"Output file size: {os.path.getsize(output_path) / 1024 / 1024:.2f} MB")

    print("\n✓ Processing completed successfully!")
    print(f"Districts GeoJSON saved to: {output_path}")