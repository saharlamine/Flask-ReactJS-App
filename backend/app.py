from flask import Flask, jsonify,request
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/flaskdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
#Create Database
class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text())
    date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, title, body):
        self.title = title
        self.body = body

ma= Marshmallow(app)

class ArticlesSchema(ma.Schema):
    class Meta:
        fields =('id','title','body','date')

article_schema = ArticlesSchema()
articles_schema = ArticlesSchema(many=True)

@app.route('/add', methods=['POST'])
def addArticles():
    title =request.json['title']
    body =request.json['body']
    articles = Articles(title,body)
    db.session.add(articles)
    db.session.commit()
    return article_schema.jsonify(articles)


@app.route('/', methods=['GET'])
def getArticles():
   all_articles = Articles.query.all()
   rst =articles_schema.dump(all_articles)
   return jsonify(rst)

@app.route('/get/<id>/', methods=['GET'])
def getArticlesById(id):
   article = Articles.query.get(id)
   return article_schema.jsonify(article)

@app.route('/update/<id>/', methods=['PUT'])
def updateArticle(id):
    article = Articles.query.get(id)
    if 'title' in request.json:
        article.title = request.json['title']
    if 'body' in request.json:
        article.body = request.json['body']
    db.session.commit()
    return article_schema.jsonify(article)

@app.route('/delete/<id>/', methods=['DELETE'])
def DeleteArticle(id):
    article = Articles.query.get(id)
    if article:
        db.session.delete(article)
        db.session.commit()
        return jsonify({"message": "Article deleted successfully"})
    else:
        return jsonify({"error": "Article not found"}), 404

# Create the database tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
