from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(500), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
        
        # Basically __repr__ me ye hota hai ki jab bhi ham koi todo ka object print kare to hame uska object print hua dikhna chahiye. to vo __repr__ se dikhega __repr__ ka matlab hai representation.
        

        # __repr__ is a special method in Python that stands for “representation”. It is used to define how an object should be represented as a string, especially when you're debugging or printing objects. 

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title = title, desc = desc )
        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.all()
    return render_template('index.html', allTodo = allTodo)
    # return 'Hello, World!'

# @app.route('/show')
# def products():
#     allTodo = Todo.query.all()
#     print(allTodo)
#     return 'this is products page'

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    allTodo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', allTodo = allTodo)

@app.route('/delete/<int:sno>')
def delete(sno):
    allTodo = Todo.query.filter_by(sno=sno).first()
    # db.session.delete(Todo)
    db.session.delete(allTodo)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)  

    #debug = true karne pr hame page pr wrong code karne par show ho jayega ki hamne kuch galat kra hai code me