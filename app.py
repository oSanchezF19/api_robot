from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Post(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    temp = db.Column(db.Float)
    hum = db.Column(db.Float)
    date = db.Column(db.String(100))

class PostSchema(ma.Schema):
    class Meta:
        fields = ('id', 'temp', 'hum', 'date')

post_schema = PostSchema()
posts_schema = PostSchema(many = True)


class PostsResource(Resource):
    def get(self):
            return posts_schema.dump(Post.query.all())  
    
    def post(self):
        try:
            data = request.json
            
            if 'hum' in data:
                post = Post(hum=data['hum'], date=datetime.now())
            if 'temp' in data:
                post = Post(temp=data['temp'], date=datetime.now())
            if 'temp' and 'hum' in data:
                post = Post(temp=data['temp'],hum=data['hum'], date=datetime.now())
            db.session.add(post)
            db.session.commit()
            return post_schema.dump(post)
        except:
            return jsonify({"mensaje:":"error en la solicitud"}), 400

class PostResource(Resource):
    def get(self, pk):
        return post_schema.dump(Post.query.get_or_404(pk))

    def put(self, pk):
        data = request.json
        post = Post.query.get_or_404(pk)

        if 'temp' in data:
            post.temp = data['temp']
        if 'hum' in data:
            post.hum = data['hum']
        if 'date' in data:
            post.date = data['date']

        db.session.commit()
        return post_schema.dump(post)

    def delete(self, pk):
        post = Post.query.get_or_404(pk)
        db.session.delete(post)
        db.session.commit()

        return '', 204

api.add_resource(PostResource, '/post/<int:pk>')
api.add_resource(PostsResource, '/posts')

if __name__ == '__main__':
    app.run(debug= True)