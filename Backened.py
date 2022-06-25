import psycopg2

from PostsHandler import PostsHandler
from UserHandler import UserHandler

db = psycopg2.connect(
    host='localhost',
    port=5432,
    user='postgres',
    password='pos-72270',
    database='bloggir'

)

cursor = db.cursor()
userHandler = UserHandler(database=db, cursor=cursor)
postHandler = PostsHandler(database=db, cursor=cursor,functions={"userPublicCredentials":userHandler.userPublicCredentials})

