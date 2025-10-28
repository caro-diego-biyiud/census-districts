import geopandas as gpd
import os
from pathlib import Path

def main():
    print("=== Spanish Census Sections Shapefile to GeoJSON Converter ===")
    print("Converting INE census sections from shapefile to GeoJSON format...\n")

    # Set up paths
    script_dir = Path(__file__).parent
    input_path = script_dir / "../data/raw/SECC_CE_20250101.shp"
    output_path = script_dir / "../data/interim/sections_2025.geojson"

    # Create interim directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Input file: {input_path}")
    print(f"Output file: {output_path}")

    # Check if input file exists
    if not input_path.exists():
        print(f"ERROR: Input shapefile not found at {input_path}")
        print("Please ensure the shapefile and all its components (.shp, .dbf, .prj, etc.) are present.")
        return

    print("\n1. Loading shapefile...")
    try:
        gdf = gpd.read_file(str(input_path))
        print(f"   ✓ Successfully loaded shapefile")
        print(f"   ✓ Records: {len(gdf):,}")
        print(f"   ✓ Fields: {len(gdf.columns)}")
        print(f"   ✓ CRS: {gdf.crs}")
        print(f"   ✓ Geometry type: {gdf.geometry.geom_type.iloc[0] if len(gdf) > 0 else 'Unknown'}")
    except Exception as e:
        print(f"ERROR loading shapefile: {e}")
        return

    print("\n2. Dataset information...")
    print(f"   Available fields: {list(gdf.columns)}")

    # Show sample of first few field values for key columns
    key_fields = ['CPRO', 'CMUN', 'CDIS', 'CUSEC'] if 'CUSEC' in gdf.columns else ['CPRO', 'CMUN', 'CDIS']
    for field in key_fields:
        if field in gdf.columns:
            sample_values = gdf[field].dropna().unique()[:5]
            print(f"   {field} sample values: {list(sample_values)}")

    print("\n3. Converting to GeoJSON...")
    try:
        # Convert and save as GeoJSON
        gdf.to_file(str(output_path), driver="GeoJSON")
        print(f"   ✓ Successfully converted to GeoJSON")
    except Exception as e:
        print(f"ERROR during conversion: {e}")
        return

    print("\n4. Validating output...")
    try:
        # Verify the output file
        if output_path.exists():
            file_size_mb = os.path.getsize(output_path) / 1024 / 1024
            print(f"   ✓ Output file created successfully")
            print(f"   ✓ File size: {file_size_mb:.2f} MB")

            # Quick validation by reading a few records
            test_gdf = gpd.read_file(str(output_path), rows=5)
            print(f"   ✓ Validation read successful: {len(test_gdf)} sample records")
        else:
            print("   ERROR: Output file was not created")
            return
    except Exception as e:
        print(f"ERROR during validation: {e}")
        return

    print("\n=== Conversion Summary ===")
    print(f"Source: {input_path.name}")
    print(f"Target: {output_path.name}")
    print(f"Records processed: {len(gdf):,}")
    print(f"Fields preserved: {len(gdf.columns)}")
    print(f"Output size: {file_size_mb:.2f} MB")
    print(f"Coordinate system: {gdf.crs}")

    print("\n✓ Conversion completed successfully!")
    print(f"GeoJSON file ready at: {output_path}")
    print("\nYou can now use this GeoJSON file for faster processing in subsequent scripts.")

if __name__ == "__main__":
    main()