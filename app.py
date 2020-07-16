from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)
ma = Marshmallow(app)

tags = db.Table('tags',
    db.Column('temp_id', db.Integer, db.ForeignKey('temp.temp_id')),
    db.Column('page_id', db.Integer, db.ForeignKey('hum.hum_id'))
)

class Temp(db.Model):
    temp_id =db.Column(db.Integer, primary_key=True)
    temp = db.Column(db.Float)
    date = db.Column(db.String(100))

class Hum(db.Model):
    hum_id =db.Column(db.Integer, primary_key=True)
    hum = db.Column(db.Float)
    date = db.Column(db.String(100))

class PostSchema(ma.Schema):
    class Meta:
        fields = ('temp_id', 'hum_id', 'temp', 'hum', 'date')

post_schema = PostSchema()
posts_schema = PostSchema(many = True)


class temperatura(Resource):
    def get(self):
            return posts_schema.dump(Temp.query.all()) 

    def post(self):
        data = request.json
        try:     
            post = Temp(temp=data['temp'], date=datetime.now())
            db.session.add(post)
            db.session.commit()
            return post_schema.dump(post)

        except:
            response = jsonify({"mensaje:":"error en la solicitud"})
            response.status_code = 400
            return response

          
class tempid(Resource):
    def get(self, pk):
        return post_schema.dump(Temp.query.get_or_404(pk))

    def put(self, pk):
        data = request.json
        post = Temp.query.get_or_404(pk)
        try:
            
            if 'temp' in data:
                post.temp = data['temp']
            if 'date' in data:
                post.date = data['date']

            db.session.commit()
            return post_schema.dump(post)

        except:
            response = jsonify({"mensaje:":"error en la solicitud"})
            response.status_code = 400
            return response

    def delete(self, pk):
        post = Temp.query.get_or_404(pk)
        db.session.delete(post)
        db.session.commit()

        return '', 204

class humedad(Resource):
    def get(self):
            return posts_schema.dump(Hum.query.all()) 

    def post(self):
        data = request.json
        try:
            post = Hum(hum=data['hum'], date=datetime.now())
            db.session.add(post)
            db.session.commit()
            return post_schema.dump(post)
        except:
            response = jsonify({"mensaje:":"error en la solicitud"})
            response.status_code = 400
            return response
          
class humid(Resource):
    def get(self, pk):
        return post_schema.dump(Hum.query.get_or_404(pk))

    def put(self, pk):
        data = request.json
        post = Hum.query.get_or_404(pk)
        try:
            if 'hum' in data:
                post.hum = data['hum']
            if 'date' in data:
                post.date = data['date']

            db.session.commit()
            return post_schema.dump(post)
        except:
            response = jsonify({"mensaje:":"error en la solicitud"})
            response.status_code = 400
            return response

    def delete(self, pk):
        post = Hum.query.get_or_404(pk)
        db.session.delete(post)
        db.session.commit()

        return '', 204

api.add_resource(temperatura, '/temp')
api.add_resource(tempid, '/temp/<int:pk>')
api.add_resource(humedad, '/hum')
api.add_resource(humid, '/hum/<int:pk>')




if __name__ == '__main__':
    app.run(debug= True)