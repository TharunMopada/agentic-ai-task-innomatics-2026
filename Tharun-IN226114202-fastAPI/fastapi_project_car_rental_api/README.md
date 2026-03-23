🚗 FastAPI Car Rental Service API
Project Overview

This project is a Car Rental Service Backend API built using FastAPI.
It allows users to browse available cars, rent vehicles, manage bookings, and perform advanced operations like search, sorting, and pagination.

The application demonstrates real-world backend concepts including REST APIs, data validation, CRUD operations, and multi-step workflows.

🚀 Features

✅ Core APIs
Home route
Get all cars
Get car by ID
Cars summary

✅ Data Validation (Pydantic)
Input validation using Pydantic models
Field constraints and error handling

✅ CRUD Operations
Add new car
Update car details
Delete car

✅ Helper Functions
Find car by ID
Calculate rental cost
Filter logic

✅ Multi-Step Workflow
Add to cart
View cart
Checkout (create rental orders)

✅ Advanced APIs
Search cars by keyword
Sort cars (price, type, etc.)
Pagination
Combined browsing (search + sort + pagination)

🛠️ Tech Stack
Python
FastAPI
Uvicorn
Pydantic
📂 Project Structure
fastapi_project_car_rental_api/
│
├── main.py
├── requirements.txt
├── README.md
└── screenshots/
▶️ How to Run the Project
1. Clone the repository
git clone https://github.com/your-username/fastapi_project_car_rental_api.git
cd fastapi_project_car_rental_api
2. Install dependencies
pip install -r requirements.txt
3. Run the server
python -m uvicorn main:app --reload
4. Open in browser
http://127.0.0.1:8000/docs
🧪 API Testing

All APIs are tested using Swagger UI.

You can:

Execute endpoints
Send request data
View responses instantly
📸 Screenshots

Screenshots of all API endpoints are available in the screenshots/ folder.

📊 Example Workflow
View available cars
Add car to cart
Checkout and create booking
View rental history
🎯 Learning Outcomes
Built RESTful APIs using FastAPI
Implemented request validation with Pydantic
Designed CRUD operations
Created multi-step workflows
Implemented search, sorting, and pagination
🔗 GitHub Repository

(Add your GitHub link here)

🙌 Acknowledgement

This project was developed as part of FastAPI training.

Special thanks to Innomatics Research Labs for guidance and support.

📌 Author

Tharun Mopada
