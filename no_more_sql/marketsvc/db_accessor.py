import logging
import sqlite3
from db.base import engine
from sqlalchemy import text
from db.init_db import DB_PATH

def execute_query(query, params):
    with sqlite3.connect(DB_PATH) as conn:
        curr = conn.cursor()
        curr.execute(query, params)
        rows = curr.fetchall()
        return rows
    
def execute_query(query, params=None):
    with engine.connect() as conn:
        return conn.execute(text(query), parameters=params)

def execute_insert_query(query, params):
    with sqlite3.connect(DB_PATH) as conn:
        curr = conn.cursor()
        curr.execute(query, params)
        result = curr.fetchone()
        conn.commit()
        return result

def execute_insert_query(query, params_tuple):
    with engine.connect() as conn:
        cursor = conn.execute(text(query), parameters=params_tuple)
        result = cursor.fetchone()
        conn.commit()
        return result

def execute_insert_queries(query, params_tuple):
    with sqlite3.connect(DB_PATH) as conn:
        curr = conn.cursor()
        curr.execute(query, params_tuple)
        conn.commit()

def execute_insert_queries(query, params_tuple):
    with engine.connect() as conn:
        conn.execute(text(query), parameters=params_tuple)
        conn.commit()

def get_customers():
    rows = execute_query(query = "SELECT * FROM customer", 
                         params = {})
    return rows

def get_orders_of_customer(customer_id):
    rows = execute_query(query = """
                    SELECT
                         item.name,
                         item.description,
                         item.price,
                         item.price*order_items.quantity AS total
                    FROM orders
                    JOIN order_items
                    ON
                         item.id = order_items.item_id
                    WHERE
                         orders.customer_id =: customer_id
""",
params={"customer_id": customer_id})
    return rows

def get_total_cost_of_an_order(order_id):
    rows = execute_query(query="""
                SELECT
                         SUM(item.price * order_items.quantity) AS total
                FROM orders
                JOIN order_items
                ON
                         order_items.order_id = orders.id
                JOIN item
                ON
                         item.id = order_items.item_id
                WHERE
                         orders.id =: order_id
""",
params={'order_id': order_id})
    return rows[0][0]


def get_orders_between_dates(after, before):
    rows = execute_query(
        query="""
        SELECT
            customer.name,
            item.name,
            item.price,
            item.price*order_items.quantity AS total
        FROM orders
        JOIN customer
        ON
            customer.id = orders.customer_id
        JOIN order_items
        ON
            order_items.order_id = orders.id
        JOIN item
        ON
            item.id = order_items.item_id
        WHERE 
            orders.order_time >= :after
        AND
            orders.order_time <= :before
""",
params={"after": after, "before":before}
    )
    return rows


def add_new_order_for_customer(customer_id, items):
    try:
        new_order_id = execute_insert_query(
            query = """
            INSERT INTO orders
                (customer_id, order_time)
            VALUES
                (:customer_id, Date('now'))
            RETURNING id
""",
params={'customer_id': customer_id})[0]
        
        execute_insert_queries("""
            INSERT INTO order_items
                    (order_id, item_id, quantity)
            VALUES
                    (:order_id, :item_id, :quantity)
""",
params_tuple = [
    {
        "order_id": new_order_id,
        "item_id": item["id"],
        "quantity": item["quantity"]
}
for item in items
])
        return True
    except Exception:
        logging.exception("Failed to add a new order")
        return False

def add_new_order_for_customer(customer_id, items):
    try:
        new_order_id = execute_insert_query(
            """
        INSERT INTO orders
            (customer_id, order_time)
        VALUES
            (:customer_id, Date('now'))
        RETURNING id
""",
{"customer_id": customer_id}
        ).id
        execute_insert_queries("""
            INSERT INTO order_items
                    (order_id, item_id, quantity)
            VALUES
                    (:order_id, :item_id, :quantity)
""",
params_tuple = [
    {
        "order_id": new_order_id,
        "item_id": item["id"],
        "quantity": item["quantity"]
}
for item in items
])
        return True
    except Exception:
        logging.exception("Failed to add a new order")
        return False
