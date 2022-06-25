from psycopg2 import sql

from BasicFuns import idGenerator


class UserHandler:
    def __init__(self, database, cursor):
        self.database = database
        self.cursor = cursor

    def addUser(self, username, name, password):
        if not self.checkUserName(username=username):
            sqlquery = sql.SQL('insert into users ({username},{name},{password},{likes},{bookmarks}) values (%s,%s,%s,%s,%s) returning user_id').format(
                userid=sql.Identifier("user_id"),
                name=sql.Identifier("name"),
                username=sql.Identifier("username"),
                password=sql.Identifier("password"),
                likes=sql.Identifier("likes"),
                bookmarks=sql.Identifier("bookmarks")
            )
            self.cursor.execute(sqlquery, (username, name, password, [], []))

            self.database.commit()
            return {"status": True, "user_id": self.cursor.fetchone()[0]}
        return {"status": False}

    def checkUserName(self, username):
        sqlquery = sql.SQL('select username from users')
        self.cursor.execute(sqlquery)
        data = self.cursor.fetchall()
        data = [i[0] for i in data] if data else []
        if username in data:
            return True
        return False

    def userPublicCredentials(self, user_id):
        sqlquery = sql.SQL('select {username},{name} from users where user_id = %s').format(
            username=sql.Identifier("username"), name=sql.Identifier("name"))
        self.cursor.execute(sqlquery,(user_id,))
        data = self.cursor.fetchone()
        return {"username": data[0], "name": data[1]} if data else {}

    def authUser(self, username, password):
        sqlquery = sql.SQL('select * from users where {username} = %s and {password} = %s').format(
            username=sql.Identifier("username"),
            password=sql.Identifier("password")
        )
        self.cursor.execute(sqlquery, (username, password))
        data = self.cursor.fetchone()
        return {"user_id": data[0], 'status': True, 'auth': True} if data else {'auth': False, 'status': True}

    def authLogin(self, username, token, client_id):
        sqlquery = sql.SQL(
            'select name from logins where {username} = %s and {token} = %s and {client_id} = %s').format(username=sql.Identifier("username"), token=sql.Identifier("token"), client_id=sql.Identifier("client_id"))
        self.cursor.execute(sqlquery, (username, token, client_id))
        data = self.cursor.fetchone()
        if data:
            return {'status': True, "auth": True}
        return {'status': False}

    def login(self, username, password):
        if self.authUser(username=username, password=password):
            token, client_id = idGenerator(), idGenerator()
            sqlquery = sql.SQL(
                'insert into logins ({username},{token},{client_id}) values (%s,%s,%s)').format(
                    username=sql.Identifier("username"),
                    token=sql.Identifier("token"),
                    client_id=sql.Identifier("client_id"))
            self.cursor.execute(sqlquery, (username, token, client_id))
            self.database.commit()
            return {'status': True, "auth": True, "token": token, "client_id": client_id}
        return {'status': False, 'auth': False}
