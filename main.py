from flask import Flask,render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    date = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f"{self.sno} - {self.title}"



@app.route("/", methods=['GET','POST'])
def home():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        entry = Todo(title=title, desc=desc)
        db.session.add(entry)
        db.session.commit()
    
    allentry = Todo.query.all()

    return render_template("index.html", alltodo=allentry)

@app.route("/update/<int:no>", methods=['GET','POST'])
def update(no):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        entry = Todo.query.filter_by(sno=no).first()
        
        entry.title = title
        entry.desc = desc
        db.session.add(entry)
        db.session.commit()
        return redirect('/')

    toupdate = Todo.query.filter_by(sno=no).first()
    

    return render_template('update.html', toup=toupdate)

@app.route("/delete/<int:no>", methods=['GET','POST'])
def delete(no):
    todelete = Todo.query.filter_by(sno=no).first()
    db.session.delete(todelete)
    db.session.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)