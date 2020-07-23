from flask import Flask, jsonify, request
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
        try:
            data = request.json 
            if  data['temp']>=100 or data['temp']<=0:
                raise IOError('temp')   
            if 'date' in data:
                if (not type(data['descripcion']) is str and not type(data['temp']) is float and type(datetime.strptime(data['date'], "%Y/%m/%d %H:%M:%S")) is datetime):
                    raise Exception ('a','descripcion','temp')
                if (not type(data['descripcion']) is str and type(datetime.strptime(data['date'], "%Y/%m/%d %H:%M:%S")) is datetime):
                    raise Exception ('descripcion')
                if (not type(data['temp']) is float and type(datetime.strptime(data['date'], "%Y/%m/%d %H:%M:%S")) is datetime):
                    raise Exception ('temp')
                post = Temp(temp=float(data['temp']), date=datetime.strptime(data['date'], "%Y/%m/%d %H:%M:%S"), descripcion=data['descripcion'])
            else:
                if (not type(data['descripcion']) is str and not type(data['temp']) is float):
                    raise Exception ('a','descripcion','temp')
                if (not type(data['descripcion']) is str):
                    raise Exception ('descripcion')
                if (not type(data['temp']) is float):
                    raise Exception ('temp')
                post = Temp(temp=float(data['temp']), date=datetime.now(), descripcion=data['descripcion'])

            db.session.add(post)
            db.session.commit()
            return post_schema.dump(post)

        except IOError as err:
            response = jsonify({err.args[0]:"debe estar ente 0 y 100"})
            response.status_code = 400
            return response

        except KeyError as err:
            response = jsonify({err.args[0]:"está mal escrito"})
            response.status_code = 400
            return response

        except Exception as err:

            if (type(data['descripcion']) is str and type(data['temp']) is float and err.args[0]=="strptime() argument 1 must be str, not int"):
                response = jsonify({"date":"Debe tener el formato 'yyyy/mm/dd hh:mm:ss'"})
                response.status_code = 400
            if (not type(data['descripcion']) is str and not type(data['temp']) is float and err.args[0]=="strptime() argument 1 must be str, not int"):
                response = jsonify({"descripcion":"debe ser tipo string", "temp" :"debe ser tipo float", "date":"Debe tener el formato 'yyyy/mm/dd hh:mm:ss'"})
                response.status_code = 400
            if (type(data['descripcion']) is str and not type(data['temp']) is float and err.args[0]=="strptime() argument 1 must be str, not int"):
                response = jsonify({"temp" :"debe ser tipo float", "date":"Debe tener el formato 'yyyy/mm/dd hh:mm:ss'"})
                response.status_code = 400
            if (not type(data['descripcion']) is str and type(data['temp']) is float and err.args[0]=="strptime() argument 1 must be str, not int"):
                response = jsonify({"descripcion":"debe ser tipo string", "date":"Debe tener el formato 'yyyy/mm/dd hh:mm:ss'"})
                response.status_code = 400
            if err.args[0]=='a':
                response = jsonify({err.args[1] :"debe ser tipo string", err.args[2] :"debe ser tipo float"})
                response.status_code = 400
            if err.args[0]=='descripcion':
                response = jsonify({err.args[0]:"debe ser tipo string"})
                response.status_code = 400
            if err.args[0]=='temp':
                response = jsonify({err.args[0]:"debe ser tipo float"})
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
                if  data['temp']>=100 or data['temp']<=0:
                    raise IOError('temp')
                if (not type(data['temp']) is float):
                    raise TypeError ('temp')
                post.temp = data['temp']

            if 'descripcion' in data:
                if (not type(data['descripcion']) is str):
                    raise TypeError ('descripcion')
                post.descripcion = data['descripcion']
            
            if 'date' in data:
                if (not type(datetime.strptime(data['date'], "%Y/%m/%d %H:%M:%S") is datetime)):
                    raise TypeError
                post.date = datetime.strptime(data['date'], "%Y/%m/%d %H:%M:%S")

            db.session.commit()
            return post_schema.dump(post)
        except IOError as err:
            response = jsonify({err.args[0]:"debe estar ente 0 y 100"})
            response.status_code = 400
            return response

        except KeyError as err:
            response = jsonify({err.args[0]:"está mal escrito"})
            response.status_code = 400
            return response

        except TypeError as err:
            if (not type(data['temp']) is float and not type(data['descripcion']) is str):
                response = jsonify({"descripcion":"debe ser tipo string","temp":"debe ser tipo float"})
            if (not type(data['temp']) is float and type(data['descripcion']) is str):
                response = jsonify({"temp":"debe ser tipo float"})
            if (not type(data['descripcion']) is str and type(data['temp']) is float):
                response = jsonify({"descripcion":"debe ser tipo string"})
            if (err.args[0]=="strptime() argument 1 must be str, not int"):
                response = jsonify({"date":"Debe ser una fecha valida en el formato 'yyyy/mm/dd hh:mm:ss'"})
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
        try:
            data = request.json 
            if  data['hum']>=100 or data['hum']<=0:
                raise IOError('hum')   
            if 'date' in data:
                if (not type(data['descripcion']) is str and not type(data['hum']) is float and type(datetime.strptime(data['date'], "%Y/%m/%d %H:%M:%S")) is datetime):
                    raise Exception ('a','descripcion','hum')
                if (not type(data['descripcion']) is str and type(datetime.strptime(data['date'], "%Y/%m/%d %H:%M:%S")) is datetime):
                    raise Exception ('descripcion')
                if (not type(data['hum']) is float and type(datetime.strptime(data['date'], "%Y/%m/%d %H:%M:%S")) is datetime):
                    raise Exception ('hum')
                post = Hum(hum=float(data['hum']), date=datetime.strptime(data['date'], "%Y/%m/%d %H:%M:%S"), descripcion=data['descripcion'])
            else:
                if (not type(data['descripcion']) is str and not type(data['hum']) is float):
                    raise Exception ('a','descripcion','hum')
                if (not type(data['descripcion']) is str):
                    raise Exception ('descripcion')
                if (not type(data['hum']) is float):
                    raise Exception ('hum')
                post = Hum(hum=float(data['hum']), date=datetime.now(), descripcion=data['descripcion'])

            db.session.add(post)
            db.session.commit()
            return post_schema.dump(post)

        except IOError as err:
            response = jsonify({err.args[0]:"debe estar ente 0 y 100"})
            response.status_code = 400
            return response

        except KeyError as err:
            response = jsonify({err.args[0]:"está mal escrito"})
            response.status_code = 400
            return response

        except Exception as err:

            if (type(data['descripcion']) is str and type(data['hum']) is float and err.args[0]=="strptime() argument 1 must be str, not int"):
                response = jsonify({"date":"Debe tener el formato 'yyyy/mm/dd hh:mm:ss'"})
                response.status_code = 400
            if (not type(data['descripcion']) is str and not type(data['hum']) is float and err.args[0]=="strptime() argument 1 must be str, not int"):
                response = jsonify({"descripcion":"debe ser tipo string", "hum" :"debe ser tipo float", "date":"Debe tener el formato 'yyyy/mm/dd hh:mm:ss'"})
                response.status_code = 400
            if (type(data['descripcion']) is str and not type(data['hum']) is float and err.args[0]=="strptime() argument 1 must be str, not int"):
                response = jsonify({"hum" :"debe ser tipo float", "date":"Debe tener el formato 'yyyy/mm/dd hh:mm:ss'"})
                response.status_code = 400
            if (not type(data['descripcion']) is str and type(data['hum']) is float and err.args[0]=="strptime() argument 1 must be str, not int"):
                response = jsonify({"descripcion":"debe ser tipo string", "date":"Debe tener el formato 'yyyy/mm/dd hh:mm:ss'"})
                response.status_code = 400
            if err.args[0]=='a':
                response = jsonify({err.args[1] :"debe ser tipo string", err.args[2] :"debe ser tipo float"})
                response.status_code = 400
            if err.args[0]=='descripcion':
                response = jsonify({err.args[0]:"debe ser tipo string"})
                response.status_code = 400
            if err.args[0]=='hum':
                response = jsonify({err.args[0]:"debe ser tipo float"})
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
                if  data['hum']>=100 or data['hum']<=0:
                    raise IOError('hum')
                if (not type(data['hum']) is float):
                    raise TypeError ('hum')
                post.hum = data['hum']

            if 'descripcion' in data:
                if (not type(data['descripcion']) is str):
                    raise TypeError ('descripcion')
                post.descripcion = data['descripcion']
            
            if 'date' in data:
                if (not type(datetime.strptime(data['date'], "%Y/%m/%d %H:%M:%S") is datetime)):
                    raise TypeError
                post.date = datetime.strptime(data['date'], "%Y/%m/%d %H:%M:%S")

            db.session.commit()
            return post_schema.dump(post)
        except IOError as err:
            response = jsonify({err.args[0]:"debe estar ente 0 y 100"})
            response.status_code = 400
            return response

        except KeyError as err:
            response = jsonify({err.args[0]:"está mal escrito"})
            response.status_code = 400
            return response

        except TypeError as err:
            if (not type(data['hum']) is float and not type(data['descripcion']) is str):
                response = jsonify({"descripcion":"debe ser tipo string","hum":"debe ser tipo float"})
            if (not type(data['hum']) is float and type(data['descripcion']) is str):
                response = jsonify({"hum":"debe ser tipo float"})
            if (not type(data['descripcion']) is str and type(data['hum']) is float):
                response = jsonify({"descripcion":"debe ser tipo string"})
            if (err.args[0]=="strptime() argument 1 must be str, not int"):
                response = jsonify({"date":"Debe ser una fecha valida en el formato 'yyyy/mm/dd hh:mm:ss'"})
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