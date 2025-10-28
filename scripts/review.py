import geopandas as gpd
import os
from pathlib import Path


def main():
    script_dir = Path(__file__).parent
    data_path = script_dir / "../data/interim/sections_2025.geojson"
    print(f"Input file: {data_path}")
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

    print(type(gdf))
    print(gdf.shape)
    print(gdf.head())


if __name__ == "__main__":
    main()
