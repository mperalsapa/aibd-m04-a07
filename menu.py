
def PrintNumberedList(list):
    if len(list) == 0:
        return
    
    startIndex = 1

    for i in range(len(list)):
        print("{} - {}".format(i + startIndex, list[i]))
        # print(i)

def PrintList(list):
    if len(list) == 0:
        return
    
    for i in range(len(list)):
        print(" - {}".format(list[i]))
        # print(i)

def PrintMenu():
    menu =[
        "Descarregar dades (Esborra els existents)",
        "Llistar productes i categories",
        "Llistar productes nous",
        "Llistar els deu productes mes cars",
        "Esborrar base de dades",
        "Sortir"
    ]
    PrintNumberedList(menu)
