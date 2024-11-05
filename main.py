import menu
import mongo
import mercadona
import log

if __name__ == "__main__":
    mongoclient = mongo.GetClient()
    client = mongoclient.mercadona

    while True:
        menu.PrintMenu()
        option = input("Introdueix una opció: ")

        match option:
            case "1":
                # Get db categories, to skip when scanning
                currentCategories = [c["parent_id"] for c in client.categories.find({}, {"_id": 0, "parent_id": 1})]
                
                # Get api data
                log.Print("Getting new data")
                categories = mercadona.FindCategories()                
                for cid in categories:
                    # If category is already in db, we skip
                    if cid in currentCategories:
                        log.Print("Skipping existing category...")
                        continue

                    # Get subcategories and products from api
                    data = mercadona.GetCategoryAndProducts(cid)
                    log.Print("Inserting new data")
                    bulk_insert = []
                    for c in data["categories"]:
                        # client.categories.insert_one(c)
                        bulk_insert.append(c)
                    client.categories.insert_many(bulk_insert)
                    log.Print("Done inserting categories")

                    bulk_insert = []
                    for p in data["products"]:
                        current_product = client.products.find_one({"id": p["id"]})
    
                        if current_product:
                            log.Print("Product already exists, merging categories")
                            # Get current existing categories of current product
                            existing_categories = current_product["categories"]
                            
                            # Extract new categories from product to insert
                            new_categories = p["categories"]  # Como es obligatorio, accedemos directamente
                            
                            # Add new categories if they are not in the list
                            for new_category in new_categories:
                                if new_category not in existing_categories:
                                    # Add the new category
                                    client.products.update_one(
                                        {"id": p["id"]},
                                        {"$addToSet": {"categories": new_category}}  # Prevents duplicates 
                                    )
                        else:
                            # Si el producto no existe, lo insertamos como nuevo
                            # client.products.insert_one(p)
                            bulk_insert.append(p)
                    client.products.insert_many(bulk_insert)
                    log.Print("Done inserting products")
            case "2":
                while True:
                    menu.PrintNumberedList([
                        "Categories",
                        "Productes",
                        "Inici"
                    ])
                    option = input("Selecciona una opcio: ")
                    match option:
                        case "1":
                            print("Llistant categories")
                            products = client.categories.find({})
                            menu.PrintList([c["name"] for c in products])
                        case "2":
                            print("Llistant productes")
                            products = client.products.find({})
                            menu.PrintList([c["name"] for c in products])
                        case "3":
                            break
            case "3":
                products = client.products.find({"is_new": True})
                if len(list(products)) == 0:
                    print("No hi ha nous productes.")

                for p in products:
                    print(" - {}".format(p["name"]))

            case "4":
                products = client.categories.find({})
                for c in products:
                    print(" id:{0} - {1}".format(c["id"], c["name"]))

                # categoria = 420
                try:
                    categoria = int(input("Introdueix una categoria: "))
                except:
                    break

                products = client.products.find({"categories.id": categoria}).sort({"unit_price": -1}).limit(10)
                for p in products:
                    print(" - [{0:.2f}€] {1} ({2})".format(p["unit_price"], p["name"], p["categories"][0]["name"]))

            case "5":
                log.Print("Clearing database...")
                client.categories.delete_many({})
                client.products.delete_many({})

            case "6":
                print("Adeu :D")
                break
            case _:
                print("No has seleccionat una opcio valida.")
