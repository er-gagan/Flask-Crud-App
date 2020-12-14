from flask import Flask, render_template, request, flash
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

app.run(debug=True)