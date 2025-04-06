from flask import Flask, render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno} - {self.title}"

# ✅ Ensure database tables are created
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method=="POST":
        title = request.form['title']
        content = request.form['content']
        todo = Todo(title=title, content=content)
        db.session.add(todo)
        db.session.commit()
    alltodo = Todo.query.all()
    
    return render_template('index.html', alltodo=alltodo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:sno>',methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        content = request.form['content']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.content = content
        db.session.add(todo)
        db.session.commit()
        
        return redirect('/')
        
        
    todo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)
    


if __name__ == "__main__":
    app.run(debug=True)
