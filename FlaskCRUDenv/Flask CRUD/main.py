from flask import Flask, render_template, request, flash, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/FlaskDB'
db = SQLAlchemy(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(50))
    Email = db.Column(db.String(80), unique=True)
    Phone = db.Column(db.String(120), unique=True)

db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        Name = request.form.get('Name')
        Email = request.form.get('Email')
        Phone = request.form.get('Phone')
        entry = Students(Name = Name, Email = Email, Phone = Phone)
        db.session.add(entry)
        db.session.commit()
        flash("Data Stored Into Database")
    return render_template("Pages/home.html")

@app.route('/show')
def show():
    data = Students.query.all()
    return render_template("Pages/show.html", data=data)

@app.route('/editPage')
def Edit():
    id = request.args.get('id')
    data = Students.query.filter_by(id = id)
    for i in data:
        session['id'] = i.id
        Name = i.Name
        Email = i.Email
        Phone = i.Phone
        return render_template("Pages/edit.html", Name=Name, Email=Email, Phone=Phone)
    
@app.route('/editData', methods=['POST'])
def EditData():
    if request.method == 'POST':
        ID = session['id']
        Name = request.form.get('Name')
        Email = request.form.get('Email')
        Phone = request.form.get('Phone')
        data = Students.query.get(ID)
        data.Name,data.Email,data.Phone = Name,Email,Phone
        db.session.commit()
        flash("Student Record Updated..")
        return redirect("/show")
    else:
        return "<h1>404 - Not Found</h1>"

@app.route('/delete')
def delete():
    id = request.args.get('id')
    Students.query.filter_by(id = id).delete()
    db.session.commit()
    flash("Student Data Successfully Delete into Database")
    return redirect("/show")

app.run(debug=True)