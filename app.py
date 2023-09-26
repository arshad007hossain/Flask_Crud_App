from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)

# Define the model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

# CRUD operations
@app.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    item = Item(name=name)
    db.session.add(item)
    db.session.commit()
    flash('Item added successfully', 'success')
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    item = Item.query.get(id)
    if request.method == 'POST':
        item.name = request.form['name']
        db.session.commit()
        flash('Item updated successfully', 'success')
        return redirect(url_for('index'))
    return render_template('update.html', item=item)

@app.route('/delete/<int:id>')
def delete(id):
    item = Item.query.get(id)
    db.session.delete(item)
    db.session.commit()
    flash('Item deleted successfully', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.secret_key = 'your_secret_key'
    app.run(debug=True)
