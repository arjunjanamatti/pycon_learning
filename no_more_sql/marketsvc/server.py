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

@app.get("/api/customers")
def customers():
    return get_customers()

@app.get("/api/orders/{cust_id}")
def orders(cust_id: int):
    return get_orders_of_customer(cust_id)

@app.get("/api/order_total/{order_id}")
def order_total(order_id: int):
    total = get_total_cost_of_an_order(order_id=order_id)
    return {'Order Total': total}

@app.get("/api/order_between_dates/{before}/{after}")
def orders_between_dates(before: str, after: str):
    return get_orders_between_dates(after=after, before=before)

@app.post("/api/add_new_order", status_code=status.HTTP_201_CREATED)
def add_new_order(json: dict = Body):
    customer_id = json.get("customer_id")
    items = json.get("items")

    success = add_new_order_for_customer(customer_id=customer_id, items=items)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
if __name__ == "__main__":
    init_db()
    uvicorn.run("server:app", host="127.0.0.1",
                port=9090, reload=True)