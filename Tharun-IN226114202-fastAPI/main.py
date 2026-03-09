from fastapi import FastAPI

app = FastAPI()

# Product data (7 products as required in Q1)
products = [

    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True},

    # Added products (Q1 requirement)
    {"id": 5, "name": "Laptop Stand", "price": 1299, "category": "Electronics", "in_stock": True},
    {"id": 6, "name": "Mechanical Keyboard", "price": 2499, "category": "Electronics", "in_stock": True},
    {"id": 7, "name": "Webcam", "price": 1899, "category": "Electronics", "in_stock": False},
]

# Home endpoint
@app.get("/")
def home():
    return {"message": "Welcome to our E-commerce API"}

# Q1 - Get all products
@app.get("/products")
def get_products():
    return {
        "products": products,
        "total": len(products)
    }

# Q2 - Filter products by category
@app.get("/products/category/{category_name}")
def get_by_category(category_name: str):

    result = []

    for p in products:
        if p["category"].lower() == category_name.lower():
            result.append(p)

    if not result:
        return {"error": "No products found in this category"}

    return {
        "category": category_name,
        "products": result,
        "total": len(result)
    }

# Q3 - Only in-stock products
@app.get("/products/instock")
def get_instock():

    available = []

    for p in products:
        if p["in_stock"] == True:
            available.append(p)

    return {
        "in_stock_products": available,
        "count": len(available)
    }

# Q4 - Store summary
@app.get("/store/summary")
def store_summary():

    in_stock_count = 0

    for p in products:
        if p["in_stock"]:
            in_stock_count += 1

    out_of_stock_count = len(products) - in_stock_count

    categories = list(set([p["category"] for p in products]))

    return {
        "store_name": "My E-commerce Store",
        "total_products": len(products),
        "in_stock": in_stock_count,
        "out_of_stock": out_of_stock_count,
        "categories": categories
    }

# Q5 - Search products by name
@app.get("/products/search/{keyword}")
def search_products(keyword: str):

    results = []

    for p in products:
        if keyword.lower() in p["name"].lower():
            results.append(p)

    if not results:
        return {"message": "No products matched your search"}

    return {
        "keyword": keyword,
        "results": results,
        "total_matches": len(results)
    }

# BONUS - Best deal and premium pick
@app.get("/products/deals")
def get_deals():

    cheapest = min(products, key=lambda p: p["price"])
    expensive = max(products, key=lambda p: p["price"])

    return {
        "best_deal": cheapest,
        "premium_pick": expensive
    }