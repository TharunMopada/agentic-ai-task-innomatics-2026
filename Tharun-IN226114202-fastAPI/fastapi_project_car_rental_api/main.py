from fastapi import FastAPI, Query, status, Response
from pydantic import BaseModel, Field

app = FastAPI()

# DATA
cars = [
    {"id": 1, "model": "Baleno", "brand": "Maruti", "type": "Hatchback", "price_per_day": 1600, "fuel_type": "Petrol", "is_available": True},
    {"id": 2, "model": "Verna", "brand": "Honda", "type": "Sedan", "price_per_day": 2300, "fuel_type": "Petrol", "is_available": True},
    {"id": 3, "model": "Seltos", "brand": "Hyundai", "type": "SUV", "price_per_day": 3200, "fuel_type": "Diesel", "is_available": True},
    {"id": 4, "model": "Innova Crysta", "brand": "Toyota", "type": "SUV", "price_per_day": 5200, "fuel_type": "Diesel", "is_available": False},
    {"id": 5, "model": "Punch EV", "brand": "Tata", "type": "SUV", "price_per_day": 3600, "fuel_type": "Electric", "is_available": True},
    {"id": 6, "model": "Audi A4", "brand": "BMW", "type": "Luxury", "price_per_day": 8500, "fuel_type": "Petrol", "is_available": True},
]

rentals = []
rental_counter = 1

# MODELS
class RentalRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    car_id: int = Field(..., gt=0)
    days: int = Field(..., gt=0, le=30)
    license_number: str = Field(..., min_length=8)
    insurance: bool = False
    driver_required: bool = False

class NewCar(BaseModel):
    model: str = Field(..., min_length=2)
    brand: str = Field(..., min_length=2)
    type: str = Field(..., min_length=2)
    price_per_day: int = Field(..., gt=0)
    fuel_type: str = Field(..., min_length=2)
    is_available: bool = True

# HELPERS
def find_car(car_id: int):
    for c in cars:
        if c["id"] == car_id:
            return c
    return None

def calculate_rental_cost(price, days, insurance, driver):
    base = price * days

    discount = 0
    if days >= 15:
        discount = base * 0.25
    elif days >= 7:
        discount = base * 0.15

    insurance_cost = 500 * days if insurance else 0
    driver_cost = 800 * days if driver else 0

    total = base - discount + insurance_cost + driver_cost
    return base, discount, insurance_cost, driver_cost, total

# DAY 1
@app.get("/")
def home():
    return {"message": "Welcome to CityDrift Car Rentals 🚗"}

@app.get("/cars")
def get_all_cars():
    available = len([c for c in cars if c["is_available"]])
    return {"cars": cars, "total": len(cars), "available_count": available}

@app.get("/cars/summary")
def cars_summary():
    cheapest = min(cars, key=lambda x: x["price_per_day"])
    expensive = max(cars, key=lambda x: x["price_per_day"])

    type_count = {}
    fuel_count = {}

    for c in cars:
        type_count[c["type"]] = type_count.get(c["type"], 0) + 1
        fuel_count[c["fuel_type"]] = fuel_count.get(c["fuel_type"], 0) + 1

    return {
        "total": len(cars),
        "available": len([c for c in cars if c["is_available"]]),
        "by_type": type_count,
        "by_fuel_type": fuel_count,
        "cheapest": cheapest,
        "most_expensive": expensive,
    }

@app.get("/cars/unavailable")
def unavailable_cars():
    return [c for c in cars if not c["is_available"]]

# DAY 3
@app.get("/cars/filter")
def filter_cars(type: str = None, brand: str = None, fuel_type: str = None,
                max_price: int = None, is_available: bool = None):
    result = cars

    if type is not None:
        result = [c for c in result if c["type"] == type]
    if brand is not None:
        result = [c for c in result if c["brand"] == brand]
    if fuel_type is not None:
        result = [c for c in result if c["fuel_type"] == fuel_type]
    if max_price is not None:
        result = [c for c in result if c["price_per_day"] <= max_price]
    if is_available is not None:
        result = [c for c in result if c["is_available"] == is_available]

    return result

@app.get("/cars/search")
def search_cars(keyword: str):
    result = [
        c for c in cars
        if keyword.lower() in c["model"].lower()
        or keyword.lower() in c["brand"].lower()
        or keyword.lower() in c["type"].lower()
    ]
    if not result:
        return {"message": f"No cars found for: {keyword}", "results": []}
    return {"keyword": keyword, "total_found": len(result), "results": result}

@app.get("/cars/sort")
def sort_cars(sort_by: str = "price_per_day"):
    if sort_by not in ["price_per_day", "brand", "type"]:
        return {"error": "Invalid sort field"}
    return sorted(cars, key=lambda x: x[sort_by])

@app.get("/cars/page")
def paginate_cars(page: int = 1, limit: int = 3):
    start = (page - 1) * limit
    end = start + limit
    return {
        "page": page,
        "limit": limit,
        "total": len(cars),
        "total_pages": -(-len(cars) // limit),
        "cars": cars[start:end]
    }

@app.get("/cars/browse")
def browse_cars(keyword: str = None, type: str = None,
                fuel_type: str = None, max_price: int = None,
                is_available: bool = None,
                sort_by: str = "price_per_day",
                order: str = "asc",
                page: int = 1, limit: int = 3):

    result = cars

    if keyword:
        result = [c for c in result if keyword.lower() in c["model"].lower()]
    if type:
        result = [c for c in result if c["type"] == type]
    if fuel_type:
        result = [c for c in result if c["fuel_type"] == fuel_type]
    if max_price:
        result = [c for c in result if c["price_per_day"] <= max_price]
    if is_available is not None:
        result = [c for c in result if c["is_available"] == is_available]

    result = sorted(result, key=lambda x: x[sort_by], reverse=(order == "desc"))

    start = (page - 1) * limit
    end = start + limit

    return {
        "keyword": keyword,
        "sort_by": sort_by,
        "order": order,
        "total": len(result),
        "page": page,
        "limit": limit,
        "total_pages": -(-len(result) // limit),
        "results": result[start:end]
    }

# VARIABLE ROUTE
@app.get("/cars/{car_id}")
def get_car(car_id: int):
    car = find_car(car_id)
    if not car:
        return {"error": "Car not found"}
    return car

# CRUD
@app.post("/cars", status_code=status.HTTP_201_CREATED)
def add_car(new_car: NewCar):
    for c in cars:
        if c["model"] == new_car.model and c["brand"] == new_car.brand:
            return {"error": "Car already exists"}

    new_id = max(c["id"] for c in cars) + 1
    car = {"id": new_id, **new_car.dict()}
    cars.append(car)
    return car

@app.put("/cars/{car_id}")
def update_car(car_id: int, price_per_day: int = None, is_available: bool = None):
    car = find_car(car_id)
    if not car:
        return {"error": "Car not found"}

    if price_per_day is not None:
        car["price_per_day"] = price_per_day
    if is_available is not None:
        car["is_available"] = is_available

    return car

@app.delete("/cars/{car_id}")
def delete_car(car_id: int):
    car = find_car(car_id)
    if not car:
        return {"error": "Car not found"}

    for r in rentals:
        if r["car_id"] == car_id and r["status"] == "active":
            return {"error": "Car has active rental"}

    cars.remove(car)
    return {"message": "Car deleted"}

# RENTALS
@app.post("/rentals")
def create_rental(data: RentalRequest):
    global rental_counter

    car = find_car(data.car_id)
    if not car:
        return {"error": "Car not found"}
    if not car["is_available"]:
        return {"error": "Car not available"}

    base, disc, ins, drv, total = calculate_rental_cost(
        car["price_per_day"], data.days, data.insurance, data.driver_required
    )

    car["is_available"] = False

    rental = {
        "rental_id": rental_counter,
        "car_id": data.car_id,
        "customer_name": data.customer_name,
        "days": data.days,
        "base_cost": base,
        "discount": disc,
        "insurance_cost": ins,
        "driver_cost": drv,
        "total_cost": total,
        "status": "active",
    }

    rentals.append(rental)
    rental_counter += 1
    return rental

@app.get("/rentals")
def get_rentals():
    return rentals

@app.get("/rentals/{rental_id}")
def get_rental(rental_id: int):
    for r in rentals:
        if r["rental_id"] == rental_id:
            return r
    return {"error": "Rental not found"}

@app.get("/rentals/active")
def active_rentals():
    return [r for r in rentals if r["status"] == "active"]

@app.get("/rentals/by-car/{car_id}")
def rentals_by_car(car_id: int):
    return [r for r in rentals if r["car_id"] == car_id]

@app.get("/rentals/search")
def search_rentals(customer_name: str):
    results = [r for r in rentals if customer_name.lower() in r["customer_name"].lower()]
    if not results:
        return {"message": f"No rentals found for: {customer_name}"}
    return {"customer_name": customer_name, "total_found": len(results), "rentals": results}

@app.get("/rentals/sort")
def sort_rentals(sort_by: str = "total_cost"):
    if sort_by not in ["total_cost", "days"]:
        return {"error": "Invalid field"}
    return sorted(rentals, key=lambda x: x[sort_by])

@app.get("/rentals/page")
def paginate_rentals(page: int = 1, limit: int = 2):
    start = (page - 1) * limit
    end = start + limit
    return {
        "page": page,
        "limit": limit,
        "total": len(rentals),
        "total_pages": -(-len(rentals) // limit),
        "rentals": rentals[start:end]
    }

# RETURN WORKFLOW
@app.post("/return/{rental_id}")
def return_car(rental_id: int):
    for r in rentals:
        if r["rental_id"] == rental_id:
            if r["status"] == "returned":
                return {"error": "Already returned"}

            r["status"] = "returned"
            car = find_car(r["car_id"])
            if car:
                car["is_available"] = True

            return r

    return {"error": "Rental not found"}