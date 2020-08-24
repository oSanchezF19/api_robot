from flask import Flask, jsonify, request, make_response
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime, date, time

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
    temp = db.Column(db.Float(100))
    date = db.Column(db.DateTime)
    descripcion = db.Column(db.String(100))

class Hum(db.Model):
    hum_id =db.Column(db.Integer, primary_key=True)
    hum = db.Column(db.Float(100))
    date = db.Column(db.DateTime)
    descripcion = db.Column(db.String(100))


class PostSchema(ma.Schema):
    class Meta:
        fields = ('temp_id', 'hum_id', 'temp', 'hum', 'date', 'descripcion')

post_schema = PostSchema()
posts_schema = PostSchema(many = True) 
    
class temperatura(Resource):
    def get(self):
            return posts_schema.dump(Temp.query.all()) 

    def post(self):
        data = request.json 
        errors=dict()
        if (not type(data['temp']) is float):
            errors['temp'] = "debe ser tipo float"  
        else:
            if  data['temp']>=100.0 or data['temp']<=0.0:
                errors['temp'] = "debe estar ente 0 y 100"  
        if (not type(data['descripcion']) is str):
            errors['descripcion'] = "debe ser tipo string"
        if 'date' in data:
            try:
                if (not type(datetime.strptime(data['date'], "%Y/%m/%d %H:%M:%S")) is datetime):
                    raise Exception ('temp')
            except Exception:
                errors['date'] = "Debe tener el formato 'yyyy/mm/dd hh:mm:ss'"
        if errors:
            response = jsonify(errors)
            response.status_code = 400
            return response 

        if 'date' in data:
            post = Temp(temp=data['temp'], date=datetime.strptime(data['date'], "%Y/%m/%d %H:%M:%S"), descripcion=data['descripcion'])
        else:
            post = Temp(temp=data['temp'], date=datetime.now(), descripcion=data['descripcion'])
        db.session.add(post)
        db.session.commit()
        return post_schema.dump(post)
          
class tempid(Resource):
    def get(self, pk):
        return post_schema.dump(Temp.query.get_or_404(pk))

    def put(self, pk):
        post = Temp.query.get_or_404(pk)
        data = request.json 
        errors=dict()
        if 'temp' in data:
            if (not type(data['temp']) is float):
                errors['temp'] = "debe ser tipo float"  
            else:
                if  data['temp']>=100.0 or data['temp']<=0.0:
                    errors['temp'] = "debe estar ente 0 y 100"  
        if 'descripcion' in data:
            if (not type(data['descripcion']) is str):
                errors['descripcion'] = "debe ser tipo string"
        if 'date' in data:
            try:
                if (not type(datetime.strptime(data['date'], "%Y/%m/%d %H:%M:%S")) is datetime):
                    raise Exception ('temp')
            except Exception:
                errors['date'] = "Debe tener el formato 'yyyy/mm/dd hh:mm:ss'"
        if errors:
            response = jsonify(errors)
            response.status_code = 400
            return response 
    
        if 'temp' in data:
            post.temp = data['temp']

        if 'descripcion' in data:
            post.descripcion = data['descripcion']
            
        if 'date' in data:
            post.date = datetime.strptime(data['date'], "%Y/%m/%d %H:%M:%S")

        db.session.commit()
        return post_schema.dump(post)

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
        errors=dict()
        if (not type(data['hum']) is float):
            errors['hum'] = "debe ser tipo float"  
        else:
            if  data['hum']>=100.0 or data['hum']<=0.0:
                errors['hum'] = "debe estar ente 0 y 100"  
        if (not type(data['descripcion']) is str):
            errors['descripcion'] = "debe ser tipo string"
        if 'date' in data:
            try:
                if (not type(datetime.strptime(data['date'], "%Y/%m/%d %H:%M:%S")) is datetime):
                    raise Exception ('hum')
            except Exception:
                errors['date'] = "Debe tener el formato 'yyyy/mm/dd hh:mm:ss'"
        if errors:
            response = jsonify(errors)
            response.status_code = 400
            return response  
        if 'date' in data:
            post = Hum(hum=float(data['hum']), date=datetime.strptime(data['date'], "%Y/%m/%d %H:%M:%S"), descripcion=data['descripcion'])
        else:
            post = Hum(hum=float(data['hum']), date=datetime.now(), descripcion=data['descripcion'])

        db.session.add(post)
        db.session.commit()
        return post_schema.dump(post)

        
class humid(Resource):
    def get(self, pk):
        return post_schema.dump(Hum.query.get_or_404(pk))

    def put(self, pk):
        post = Hum.query.get_or_404(pk)
        data = request.json 
        errors=dict()
        if 'hum' in data:
            if (not type(data['hum']) is float):
                errors['hum'] = "debe ser tipo float"  
            else:
                if  data['hum']>=100.0 or data['hum']<=0.0:
                    errors['hum'] = "debe estar ente 0 y 100"  
        if 'descripcion' in data:
            if (not type(data['descripcion']) is str):
                errors['descripcion'] = "debe ser tipo string"
        if 'date' in data:
            try:
                if (not type(datetime.strptime(data['date'], "%Y/%m/%d %H:%M:%S")) is datetime):
                    raise Exception ('hum')
            except Exception:
                errors['date'] = "Debe tener el formato 'yyyy/mm/dd hh:mm:ss'"
        if errors:
            response = jsonify(errors)
            response.status_code = 400
            return response

        if 'hum' in data:
            post.hum = data['hum']

        if 'descripcion' in data:
            post.descripcion = data['descripcion']
            
        if 'date' in data:
            post.date = datetime.strptime(data['date'], "%Y/%m/%d %H:%M:%S")

        db.session.commit()
        return post_schema.dump(post)

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