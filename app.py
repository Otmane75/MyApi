from flask import Flask
import gestionDB as db
from flask_restful import Api
from flask_restful import Resource,reqparse

app = Flask(__name__)
api = Api(app)



class getConta(Resource):
    
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('param', type=str, required=True)
        super(getConta, self).__init__()

    def get(self):
        contacts = db.lire_contacts()
        return contacts

    def post(self):
        args = self.parser.parse_args()
        arg1 = args['param']
        certificat=db.lire_certificat(int(arg1))
        # Logique pour créer un nouvel utilisateur
        #return {'user_id': param, 'name': 'John Doe'}
        return certificat
api.add_resource(getConta, '/contacts', '/contacts/<int:param>')






@app.route('/')
def hello():
    contacts = db.lire_contacts()
    return contacts

if __name__ == '__main__':
    app.run()
