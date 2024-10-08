from flask import Flask, render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

@app.route("/")
def index():
    todo_list = Todo.query.all()
    return render_template("index.html",todo_list = todo_list)

@app.route("/add" , methods = ["POST"])
def add():
    title = request.form.get('title')
    if (len(title) == 0):
        return redirect(url_for("index"))
    new_todo = Todo(title = title , complete = False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()  
    todo.complete = not todo.complete  
    db.session.commit()  
    return redirect(url_for("index"))

@app.route("/delete/<int:todo_id>", methods=["POST"])
def delete(todo_id):
    todo = Todo.query.get(todo_id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for("index"))

@app.route("/deleteAll" , methods = ["POST"])
def deleteAll():
    Todo.query.delete()
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist
    port = int(os.environ.get('PORT', 5000))  # Use the PORT environment variable or default to 5000
    app.run(host='0.0.0.0', port=port)

