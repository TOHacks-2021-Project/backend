import requests

largeStores = [
"Budget Foods", 
"Buy-Low Foods", 
"Nesters", 
"Quality Foods", 
"Shop n' Save", 
"AG Foods", 
"Choices Markets", 
"Nature’s Fare Markets", 
"Bulkley Valley Wholesale", 
"PriceSmart Foods", 
"Save-On-Foods", 
"Atlantic Cash & Carry", 
"Atlantic Superstore", 
"Dominion", 
"Les Entrepôts Presto", 
"Extra Foods", 
"Fortinos", 
"Freshmart", 
"Loblaws", 
"Lucky Dollar Foods", 
"Maxi / Maxi & Cie", 
"NG Cash & Carry", 
"No Frills", 
"Provigo", 
"Real Canadian Superstore", 
"Shop Easy Foods", 
"Shoppers Drug Mart / Pharmaprix", 
"SuperValu", 
"T & T Supermarket", 
"Valu-mart", 
"Wholesale Club", 
"Your Independent Grocer", 
"Zehrs Markets", 
"Food Basics", 
"Marché Adonis", 
"Marché AMI", 
"Marché Extra", 
"Marché Richelieu", 
"Metro", 
"Super C", 
"Lawtons", 
"FreshCo", 
"IGA", 
"Marché Bonichoix", 
"Marché Tradition", 
"Price Chopper", 
"Rachelle-Béry", 
"Safeway", 
"Sobeys", 
"Thrifty Foods", 
"Farm Boy", 
"Longo's", 
"Coleman's", 
"Valu Foods", 
"Village Food Stores", 
"Coppa's Fresh Market", 
"Country Grocer", 
"Fairway", 
"Family Foods", 
"Foodex", 
"FoodFare", 
"Fresh City Market", 
"Freson Bros", 
"Galleria", 
"Goodness Me!", 
"Grande Cheese", 
"H Mart", 
"Highland Farms", 
"L&M", 
"Lalumière Bonanza", 
"Le Marché Esposito", 
"Le Marché Végétarien",
"Les Arpents Verts", 
"Lucky Supermarket", 
"Mike Dean Local Grocer", 
"Nations Fresh Food", 
"Nature's Emporium", 
"The North West Company", 
"Northern", 
"NorthMart", 
"SuperValu", 
"TaiKo", 
"Vince's Market", 
"Costco", 
"Dollarama", 
"IKEA", 
"Jean Coutu Group", 
"Walmart", 
"Whole Foods", 
"Giant Tiger", 
"M&M", 
"Bulk Barn", 
]

def getStores(apiKey, lat, lng, radius=5000, smallStores=True, categories=["600-6300-0066", "600-6300-0363", "600-6300-0364", "600-6900-0247"]):
    r = requests.get(
        f"https://browse.search.hereapi.com/v1/browse?"
        f"apiKey={apiKey}"
        f"&at={lat},{lng}"
        f"&in=circle:{lat},{lng};r={radius}"
        f"&categories={','.join(categories)}"
    )

    if r.status_code != 200:
        raise Exception(f"Loc API failed, CODE: {r.status_code}, RES: {r.content}")

    res = r.json()
    stores = []

    for s in res["items"]:
        try:
            if smallStores and any([x.lower() in s["title"].lower() for x in largeStores]):
                continue
            storeInfo = {}
            storeInfo["name"] = s["title"]
            storeInfo["id"] = s["id"]
            storeInfo["address"] = s["address"]
            storeInfo["pos"] = s["position"]
            storeInfo["dist"] = s["distance"]
            storeInfo["categories"] = [x["name"] for x in s["categories"]]
            
            storeInfo["web"] = None
            if "contacts" in s.keys():
                if s["contacts"]:
                    if "www" in s["contacts"][0].keys():
                        if s["contacts"][0]["www"]:
                            if "value" in s["contacts"][0]["www"][0]:
                                storeInfo["web"] = s["contacts"][0]["www"][0]["value"]

            storeInfo["isOpen"] = False
            if "openingHours" in s.keys():
                if s["openingHours"]:
                    if "isOpen" in s["openingHours"][0]:
                        storeInfo["isOpen"] = s["openingHours"][0]["isOpen"]

            stores.append(storeInfo)
        except Exception as e:
            print(f"ERROR WHILE PROCESSING MAPS! ERROR: {e}")

    stores.sort(key=lambda x: (not x["isOpen"], storeInfo["dist"]))
    return stores
