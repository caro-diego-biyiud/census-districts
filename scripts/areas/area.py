from with_districts import area_with_districts
from with_municipalities import area_with_municipalities
from only_area import total_area
from pathlib import Path


def main():
    # Set up paths
    script_dir = Path(__file__).parent
    data_areas_dir = script_dir / "../../data/areas"

    # Example: Barcelona Metropolitan Area
    # barcelona_csv = data_areas_dir / "Area_Metropolitana_Barcelona.csv"
    # if barcelona_csv.exists():
    #     print("Processing Barcelona Metropolitan Area...")
    #     area_with_districts(barcelona_csv)
    #     area_with_municipalities(barcelona_csv)
    #     total_area(barcelona_csv)

    # Example: Canary Islands (if CSV exists)
    # canary_csv = data_areas_dir / "Mancomunidad_Sureste_GC.csv"
    # if canary_csv.exists():
    #     print("Processing Canary Islands...")
    #     area_with_districts(canary_csv)
    #     area_with_municipalities(canary_csv)
    #     total_area(canary_csv)

    # Process all CSV files in the areas directory
    print("\nProcessing all available area CSV files...")
    for csv_file in data_areas_dir.glob("*.csv"):
        print(f"\n{'='*50}")
        print(f"Processing: {csv_file.name}")
        print(f"{'='*50}")
        try:
            area_with_districts(csv_file)
            area_with_municipalities(csv_file)
            total_area(csv_file)
        except Exception as e:
            print(f"ERROR processing {csv_file.name}: {e}")
            continue


if __name__ == "__main__":
    main()
