from fastapi import FastAPI
from pydantic import BaseModel  

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None
    price: float

products = []
next_id = 1

def get_product_by_id(product_id):
        for p in products:
            if p["id"] == product_id:
                return p

        return None

@app.get("/")
def read_root():
    return {"Hello": "World"}

# Read all products
@app.get("/products/")
def read_products():
    return {"products": products}

# Read a specific product by ID
@app.get("/products/{product_id}")
def read_product(product_id: int, q: str = None):
    return get_product_by_id(product_id)

# create a new product
@app.post("/products/")
def create_product(item: Item):
    global next_id
    new_product = {
        "id": next_id,
        "name": item.name,
        "description": item.description,
        "price": item.price
    }
    products.append(new_product)
    next_id += 1
    return new_product

# update an existing product
@app.put("/products/{product_id}")
def update_product(product_id: int, item: Item):
    product = get_product_by_id(product_id)
    if product is None:
        return {"error": "Product not found"}
    product["name"] = item.name
    product["description"] = item.description
    product["price"] = item.price
    return product

# delete a product
@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    deleted_product = get_product_by_id(product_id)
    global products
    products = [p for p in products if p["id"] != product_id]
    return deleted_product