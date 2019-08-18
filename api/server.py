from flask import Flask, session, request
from flask_restful import Resource, Api
from flask_cors import CORS

from database.Database import Database

app = Flask(__name__)
app.secret_key = "TONTON"
CORS(app, supports_credentials=True)
api = Api(app)

class Session(Resource):
    def get(self):
        if 'logged_in' in session:
            id = session['id']
            username = session['username']
            return {'status':True, 'user_id':id, 'username':username}
        else:
            return {'status':False, 'message':'not logged'}

class Login(Resource):
    def post(self):
        username = request.form['username']
        password = request.form['password']

        if username and password:
            user = Database().get_user(username, password)
            if user:
                session['logged_in'] = True
                session['id'] = user['id']
                session['username'] = user['username']
                return {'status': True}
            else:
                return {'status':False, 'message':'password invalid'}
        else:
            return {'status':False, 'message':'invalid form'}, 400


class Signup(Resource):
    def post(self):
        username = request.form['username']
        password = request.form['password']

        if username and password:
            if not self.check_duplicate_user(username):
                id = Database().add_user(username, password)
                session['logged_in'] = True
                session['id'] = id
                session['username'] = username
                return {'status': True}, 201
            else:
                return {'status': False, 'message':'user alredy exist'}, 200
        else:
            return {'status':False, 'message':'invalid form'}, 400
            
    
    def check_duplicate_user(self, username):
        users = Database().get_users()
        for user in users:
            if user['username'] == username:
                return True
        return False
class Logout(Resource):
    def get(self):
        session.pop('logged_in', None)
        session.pop('id', None)
        session.pop('username', None)
        return {'status': True}


api.add_resource(Session, '/api/session')
api.add_resource(Login, '/api/session/login')
api.add_resource(Signup, '/api/session/signup')
api.add_resource(Logout, '/api/session/logout')


if __name__ == "__main__":
    app.run()
