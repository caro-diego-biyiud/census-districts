from with_districts import area_with_districts
from with_municipalities import area_with_municipalities
from only_area import total_area


def main():
    # barcelona_metropololitan_area = ["Badalona",
    #                                  "Badia del Vallès",
    #                                  "Barberà del Vallès",
    #                                  "Barcelona",
    #                                  "Begues",
    #                                  "Castellbisbal",
    #                                  "Castelldefels",
    #                                  "Cerdanyola del Vallès",
    #                                  "Cervelló",
    #                                  "Corbera de Llobregat",
    #                                  "Cornellà de Llobregat",
    #                                  "Papiol, El",
    #                                  "Prat de Llobregat, El",
    #                                  "Esplugues de Llobregat",
    #                                  "Gavà",
    #                                  "Hospitalet de Llobregat, L'",
    #                                  "Palma de Cervelló, La",
    #                                  "Molins de Rei",
    #                                  "Montcada i Reixac",
    #                                  "Montgat",
    #                                  "Pallejà",
    #                                  "Ripollet",
    #                                  "Sant Adrià de Besòs",
    #                                  "Sant Andreu de la Barca",
    #                                  "Sant Boi de Llobregat",
    #                                  "Sant Climent de Llobregat",
    #                                  "Sant Cugat del Vallès",
    #                                  "Sant Feliu de Llobregat",
    #                                  "Sant Joan Despí",
    #                                  "Sant Just Desvern",
    #                                  "Sant Vicenç dels Horts",
    #                                  "Santa Coloma de Cervelló",
    #                                  "Santa Coloma de Gramenet",
    #                                  "Tiana",
    #                                  "Torrelles de Llobregat",
    #                                  "Viladecans"]

    # area_with_districts("Area_Metropolitana_Barcelona",
    #                     barcelona_metropololitan_area)
    # area_with_municipalities(
    #     "Area_Metropolitana_Barcelona", barcelona_metropololitan_area)
    # total_area("Area_Metropolitana_Barcelona", barcelona_metropololitan_area)

    canary_islands_name = "Mancomunidad_Sureste_GC"
    canary_islands = ["Agüimes", "Ingenio", "Santa Lucía de Tirajana"]

    area_with_districts(canary_islands_name,
                        canary_islands)
    area_with_municipalities(
        canary_islands_name, canary_islands)
    total_area(canary_islands_name, canary_islands)


if __name__ == "__main__":
    main()
