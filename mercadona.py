import requests
import log

def ApiRequest(url = ""):
    if not url:
        return
    
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error recuperant dades de l'api: {e}")
    return None

def FindCategories():
    categoriesJson = ApiRequest("https://tienda.mercadona.es/api/categories/")
    categories_id_list = []

    for r in categoriesJson["results"]:
        for c in r["categories"]:
            categories_id_list.append(c["id"])
    return categories_id_list

def GetCategory(category_id = 112):
    categoriesJson = ApiRequest("https://tienda.mercadona.es/api/categories/{:d}/".format(category_id))
    categories = []
    log.Print("Scanning categories")
        
    for c in categoriesJson["categories"]:
        
        log.Print("Detected category: [{}] {}".format(c["id"], c["name"]))
        categories.append(c)
    return categories

def GetCategoryAndProducts(category_id = 112):
    categoriesJson = ApiRequest("https://tienda.mercadona.es/api/categories/{:d}/".format(category_id))
    categories = []
    products = []
    log.Print("Scanning categories")
        
    for c in categoriesJson["categories"]:
        log.Print("Detected category: [{}] {}".format(c["id"], c["name"]))
        category = {
            "id": c["id"],
            "parent_id": category_id,
            "name": c["name"],
        }
        categories.append(category)
        for p in c["products"]:
            log.Print("Detected product: [{}] {}".format(p["id"], p["display_name"]))
            try: 
                product = {
                    "id": float(p["id"]),
                    "name": p["display_name"],
                    "is_new": p["price_instructions"]["is_new"],
                    "bulk_price": float(p["price_instructions"]["bulk_price"]),
                    "unit_price": float(p["price_instructions"]["unit_price"]),
                    "reference_price": float(p["price_instructions"]["reference_price"]),
                    "categories": [{
                        "id": c["id"],
                        "name": c["name"]
                    }]
                }
                products.append(product)
            except Exception as e:
                log.Print("Error parsing product: ", e)
                log.Print(p)


    return {"categories": categories, "products": products}

if __name__ == "__main__":
    categories = FindCategories()
    for cid in categories:
        data = GetCategoryAndProducts(cid)
        for c in data["categories"]:
            print(c["name"])
        for p in data["products"]:
            print(p["name"])
    # for c in FindCategories():
    #     print(c)
    
    