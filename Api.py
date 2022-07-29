from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from Backened import postHandler, userHandler

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post('/user/available')
def checkAvailabity(req: Request):
    return {'found': userHandler.checkUserName(username=req.headers.get('username'))}


@app.post('/user/add')
def addUser(req: Request):
    return userHandler.addUser(username=req.headers.get('username'), name=req.headers.get("name"), password=req.headers.get("password"))


@app.post('/user/loginAuth')
def userLogintAuth(req: Request):
    return userHandler.authLogin(username=req.headers.get('username'), token=req.headers.get('token'), client_id=req.headers.get('client_id'))


@app.post('/user/auth')
def auth(req: Request):
    return userHandler.authUser(username=req.headers.get('username'), password=req.headers.get("password"))


@app.post('/user/login')
def userLogin(req: Request):
    return userHandler.login(username=req.headers.get("username"), password=req.headers.get('password'))


@app.get('/posts/all')
def allPosts():
    return postHandler.getAllPosts()


@app.get("/post/{slug}")
def getPostBySlug(req: Request,slug):
    postHandler.postViewed(slug=slug)
    return postHandler.getPostBySlug(slug=slug)
