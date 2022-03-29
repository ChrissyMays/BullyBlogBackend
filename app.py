from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://maaqrygmbjwmts:477002a4f25d1f2a4a45c8f2bd999887dd91692e13acabcec58a7cf1583533b3@ec2-3-229-161-70.compute-1.amazonaws.com:5432/d3pei289ekbdte"

db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)

class BlogPosts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    text = db.Column(db.String, nullable=False)

    def __init__(self, title, author, text):
        self.title = title
        self.author = author
        self.text = text
        

class BlogSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "author", "text")

blog_schema = BlogSchema()
multiple_blog_schema = BlogSchema(many=True)

@app.route("/blog/add", methods=["POST"])
def add_blog():
    if request.content_type != "application/json":
        return jsonify("ERROR: Data must be sent as JSON")

    post_data = request.get_json() 
    title = post_data.get("title")
    author = post_data.get("author")
    text = post_data.get("text")  

    record = BlogPosts(title, author, text)
    db.session.add(record)
    db.session.commit()

    return jsonify(blog_schema.dump(record))

@app.route("/blog/all", methods=["GET"])
def all():
    records = db.session.query(BlogPosts).all()
    return jsonify(multiple_blog_schema.dump(records))

@app.route("/blog/get/ <id>", methods=["GET"])
def get_blog_by_id(id):
    record = db.session.query(BlogPosts).filter(BlogPosts.id == id).first()
    return jsonify(blog_schema.dump(record))

@app.route("/blog/update", methods=["PUT"])
def update_blog_by_id(id):
    record = db.session.query(BlogPosts).first()
    if record is None:
        return jsonify("Error Blog has not been initialized")

    if request.content_type != "application/json":
        return jsonify("ERROR: Data must be sent as json")

    put_data = request.get_json() 
    blog = put_data.get("blog")

    record.blog = blog
    db.session.commit()

    return jsonify(blog_schema.dump(record))


@app.route("/blog/delete/<id>", methods=["DELETE"])
def delete_blog(id):
    record = db.session.query(Reminder).filter(Reminder.id == id).first()


    db.session.delete(record)
    db.session.commit()

    return jsonify ("Blog deleted")
     
if __name__ == "__main__":
    app.run(debug=True, port=8080)