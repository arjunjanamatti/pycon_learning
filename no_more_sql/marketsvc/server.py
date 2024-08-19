import uvicorn
from db.init_db import init_db
from db_accessor import(
    add_new_order_for_customer,
    get_customers, 
    get_orders_between_dates,
    get_orders_of_customer,
    get_total_cost_of_an_order
)
from fastapi import Body, FastAPI,HTTPException, status

app = FastAPI(debug=True)

@app.get("/")
def hello():
    return "Welcome to Marketplace!"

