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
    ccaa_codigos = [
    "01", "02", "03", "04", "05", "06", "07", "08", "09",
    "10", "11", "12", "13", "14", "15", "16", "17", "18", "19"
    ]

    for cca in ccaa_codigos:
        
        main(cca)