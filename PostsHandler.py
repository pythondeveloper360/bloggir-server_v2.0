from psycopg2 import sql


class PostsHandler:
    def __init__(self, database, cursor, functions: dict):
        self.functions = functions
        self.database = database
        self.cursor = cursor

    def checkPostSlug(self, slug):
        sqlquery = sql.SQL('select slug from posts')
        self.cursor.execute(sqlquery)
        data = self.cursor.fetchall()
        data = [i[0] for i in data] if data else []
        if slug in data:
            return True
        return False

    def insertPost(self, author_id, title, tagline, content, slug):
        if not self.checkPostSlug(slug=slug):
            sqlquery = sql.SQL('insert into posts ({title},{tagline},{author_id},{content},{slug},like_num) values (%s,%s,%s,%s,%s,0)').format(
                _id=sql.Identifier("id"),
                title=sql.Identifier("title"),
                tagline=sql.Identifier("tagline"),
                content=sql.Identifier("content"),
                slug=sql.Identifier("slug"),
                author_id=sql.Identifier("author_id")
            )
            self.cursor.execute(
                sqlquery, (title, tagline, author_id, content, slug))
            self.database.commit()
            return {'status': True}
        return {'status': False}

    def getAllPosts(self):
        sqlquery = sql.SQL("select * from posts")
        self.cursor.execute(sqlquery)
        data = self.cursor.fetchall()
        return [{**{"id":i[0],'title': i[1], 'tagline':i[2], "likeNo":i[4], 'slug':i[6]}, **self.functions.get("userPublicCredentials")(i[3])} for i in data]

    def getPostBySlug(self, slug):
        sqlquery = sql.SQL(
            'select * from posts where {slug} = %s').format(slug=sql.Identifier("slug"))
        self.cursor.execute(sqlquery, (slug,))
        data = self.cursor.fetchone()
        return {**{'title': data[1], "tagline": data[2], "likeNum": data[4], 'content': data[5]}, **self.functions.get("userPublicCredentials")(data[3])} if data else {}

    def getViews(self, slug):
        sqlquery = sql.SQL('select views from posts where {slug} = %s').format(
            slug=sql.Identifier("slug"))
        self.cursor.execute(sqlquery, (slug,))
        data = self.cursor.fetchone()
        return int(data[0]) if data else 0

    def postViewed(self, slug, byUser=''):
        views = self.getViews(slug=slug)
        sqlquery = sql.SQL('update posts set {views} = %s where {slug} = %s').format(
            views=sql.Identifier("views"),
            slug = sql.Identifier("slug")
            )
        self.cursor.execute(sqlquery,(int(views+1),slug))
        self.database.commit()
