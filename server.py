from fastapi import FastAPI
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse 
from data import users
from data import products

products_requests = []

app = FastAPI()

app.mount("/static", StaticFiles(directory="static", html = True), name="static")

@app.get("/login/{user_id}/{password}")
async def login(user_id, password):
    print("Is Valid User : ", isValidUser(user_id, password))
    return {"is_success": isValidUser(user_id, password)}

@app.get("/getUser/{user_id}")
async def getUserRequest(user_id):
    user = getUser(user_id)
    response = {}
    response['id'] = user[0]
    response['name'] = user[1]
    response['email'] = user[2]
    response['phone'] = user[4]
    response['address'] = user[5]
    return {"user": response}
    
@app.get("/requestProduct/{user_id}/{owner}/{product}")
async def requestProduct(user_id, owner, product):
    id = get_request_id()
    products_requests.append((id, user_id, owner, product, 0))
    print('Requests : ', products_requests)
    return {"is_success": True}

@app.get("/makeOrder/{request_id}/{type}")
async def approveProduct(request_id, type):
    index = 0
    print(products_requests)
    for request in products_requests:
        id, user_id, owner, product_id, status = request
        if int(request_id) == int(id):
            products_requests[index] = (request_id, user_id, owner, product_id, type)
            print(products_requests)
            return {"is_success": True}
        index += 1    
    return {"is_success": False}

@app.get("/getInfoProducts/{user_id}")        
async def getInfoProducts(user_id):
    products = getProductsByRequestedUser(user_id)
    print(products)
    if len(products) > 0:
        reponse_products=[]
        for product in products:
            response = {}
            response['request_id'] = product[0]
            response['user_id'] = getUser(product[1])[1]
            response['user_phone'] = getUser(product[1])[4]
            response['owner'] = product[2]
            response['product'] = getProduct(product[3])[1]
            response['status'] = product[4]
            reponse_products.append(response)
            print('Response')
            print(reponse_products)
        return {"is_success": True, "products": reponse_products}
    return {"is_success": False}

@app.get("/getRequestedProducts/{user_id}")        
async def getProductRequest(user_id):
    products = getProductsByUser(user_id)
    if len(products) > 0:
        reponse_products=[]
        for product in products:
            response = {}
            response['request_id'] = product[0]
            response['user_id'] = getUser(product[1])[1]
            response['owner'] = product[2]
            response['product'] = getProduct(product[3])[1]
            response['status'] = product[4]
            reponse_products.append(response)
        return {"is_success": True, "products": reponse_products}
    return {"is_success": False}

def get_request_id():
    return len(products_requests) + 1

def get_request_by_id(id):
    for request in products_requests:
        product_id, _, _, _ = request
        if product_id == id:
            return request
    return None

def isValidUser(id, password):
    for user in users:
        user_id, _, _, user_password,_,_ = user
        print(user_id, user_password)
        if int(id) == user_id and password == user_password:
            return True
    return False

def getUser(id):
    for user in users:
        user_id, _, _, user_password,_,_ = user
        if user_id == int(id):
            return user
        
def getProduct(id):
    for product in products:
        product_id, _, _, _, = product
        if product_id == int(id):
            return product

def getProductsByUser(id):
    arr=[]
    for product in products_requests:
        _,_,owner_id,_,_= product
        if int(owner_id) == int(id):
            arr.append(product)
    return arr

def getProductsByRequestedUser(id):
    arr=[]
    for product in products_requests:
        _,user_id,_,_,_= product
        if int(user_id) == int(id):
            arr.append(product)
    return arr