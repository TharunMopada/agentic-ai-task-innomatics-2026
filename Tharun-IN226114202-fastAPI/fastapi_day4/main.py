from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Sample Products
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 299, "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "in_stock": True},
]

# Cart and Orders storage
cart = []
orders = []
order_id_counter = 1


class CheckoutRequest(BaseModel):
    customer_name: str
    delivery_address: str


def find_product(product_id):
    for product in products:
        if product["id"] == product_id:
            return product
    return None


def calculate_subtotal(product, quantity):
    return product["price"] * quantity


# Add item to cart
@app.post("/cart/add")
def add_to_cart(product_id: int, quantity: int = 1):

    product = find_product(product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if not product["in_stock"]:
        raise HTTPException(
            status_code=400,
            detail=f"{product['name']} is out of stock"
        )

    # check if product already in cart
    for item in cart:
        if item["product_id"] == product_id:
            item["quantity"] += quantity
            item["subtotal"] = calculate_subtotal(product, item["quantity"])
            return {
                "message": "Cart updated",
                "cart_item": item
            }

    # new item
    new_item = {
        "product_id": product_id,
        "product_name": product["name"],
        "quantity": quantity,
        "unit_price": product["price"],
        "subtotal": calculate_subtotal(product, quantity)
    }

    cart.append(new_item)

    return {
        "message": "Added to cart",
        "cart_item": new_item
    }


# View Cart
@app.get("/cart")
def get_cart():

    if not cart:
        return {"message": "Cart is empty"}

    grand_total = sum(item["subtotal"] for item in cart)

    return {
        "items": cart,
        "item_count": len(cart),
        "grand_total": grand_total
    }


# Remove item
@app.delete("/cart/{product_id}")
def remove_item(product_id: int):

    for item in cart:
        if item["product_id"] == product_id:
            cart.remove(item)
            return {"message": "Item removed from cart"}

    raise HTTPException(status_code=404, detail="Item not found in cart")


# Checkout
@app.post("/cart/checkout")
def checkout(data: CheckoutRequest):

    global order_id_counter

    if not cart:
        raise HTTPException(
            status_code=400,
            detail="Cart is empty — add items first"
        )

    orders_placed = []

    for item in cart:
        order = {
            "order_id": order_id_counter,
            "customer_name": data.customer_name,
            "product": item["product_name"],
            "quantity": item["quantity"],
            "total_price": item["subtotal"],
            "delivery_address": data.delivery_address
        }

        orders.append(order)
        orders_placed.append(order)
        order_id_counter += 1

    grand_total = sum(item["subtotal"] for item in cart)

    cart.clear()

    return {
        "message": "Checkout successful",
        "orders_placed": orders_placed,
        "grand_total": grand_total
    }


# View orders
@app.get("/orders")
def get_orders():
    return {
        "orders": orders,
        "total_orders": len(orders)
    }