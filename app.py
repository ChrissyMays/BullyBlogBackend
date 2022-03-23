from xml.etree.ElementTree import XML
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = ""

db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)

class BlogPosts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    text = db.Column(db.String, nullable=False)

    def __init__(self,  user):
        self.user = user

class BlogSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "author", "text")

blog_schema = BlogSchema()
multiple_blog_schema = BlogSchema(many=True)
     
if __name__ == "__main__":
    app.run(debug=True, port=8080)