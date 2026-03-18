from fastapi import FastAPI, Query, HTTPException
from typing import Optional, List

app = FastAPI()

# Sample Data
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics"},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery"},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics"},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery"},
    {"id": 5, "name": "Keyboard", "price": 1299, "category": "Electronics"},
]

orders = []


#  1. Home Route
@app.get("/")
def home():
    return {"message": "FastAPI Assignment Running"}


#  2. Get All Products
@app.get("/products")
def get_products():
    return products


#  3. Search Products
@app.get("/products/search")
def search_products(name: Optional[str] = None):
    if not name:
        return products
    return [p for p in products if name.lower() in p["name"].lower()]


#  4. Filter by Category
@app.get("/products/filter")
def filter_products(category: Optional[str] = None):
    if not category:
        return products
    return [p for p in products if p["category"].lower() == category.lower()]


#  5. Sort Products
@app.get("/products/sort")
def sort_products(order: str = Query("asc", enum=["asc", "desc"])):
    return sorted(products, key=lambda x: x["price"], reverse=(order == "desc"))


#  6. Pagination
@app.get("/products/paginate")
def paginate_products(limit: int = 2, offset: int = 0):
    return products[offset: offset + limit]


#  7. Get Product by ID
@app.get("/products/{product_id}")
def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")


#  8. Create Order
@app.post("/orders")
def create_order(product_ids: List[int]):
    selected_products = [p for p in products if p["id"] in product_ids]

    if not selected_products:
        raise HTTPException(status_code=400, detail="Invalid product IDs")

    total_price = sum(p["price"] for p in selected_products)

    order = {
        "order_id": len(orders) + 1,
        "items": selected_products,
        "total_price": total_price
    }

    orders.append(order)
    return order


# 9. Get All Orders
@app.get("/orders")
def get_orders():
    return orders