from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///Memo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO']=True

db = SQLAlchemy(app)

class Memo(db.Model):
    __tablename__ = 'Memo'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.Date, nullable=False, default=datetime.now().date())


@app.before_first_request
def init():
    db.create_all()


@app.route('/', methods=['GET'])
def index():
    datas = Memo.query.all()
    return render_template('index.html', memos=datas)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == "POST":
        text = request.form.get('text')
        author = request.form.get('author')
        # BlogArticleのインスタンスを作成
        memo = Memo(text=text, author=author)
        db.session.add(memo)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('create.html')


if __name__ == '__main__':
    app.run(debug=True)