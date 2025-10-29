from with_districts import cca_with_districts
from with_municipalities import cca_with_municipalities
from pathlib import Path

def main(cca):
    script_dir = Path(__file__).parent
    
    print(f"\nProcessing CCA {cca} ...")
    try:
        cca_with_districts(cca)
        cca_with_municipalities(cca)
    except Exception as e:
        print(f"ERROR processing {cca}: {e}")
        




if __name__ == "__main__":
    main("09")