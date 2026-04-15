from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bakery.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key_here'

db = SQLAlchemy(app)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Order {self.customer_name}>'


with app.app_context():
    db.create_all()
    print("База данных успешно создана!")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/orders', methods=['GET', 'POST'])
def orders():
    if request.method == 'POST':
        
        name = request.form['name']
        product = request.form['product']
        quantity = request.form['quantity']
        
        
        new_order = Order(customer_name=name, product_name=product, quantity=quantity)
        db.session.add(new_order)
        db.session.commit()
        
        return redirect(url_for('orders'))
    
    
    all_orders = Order.query.all()
    return render_template('orders.html', orders=all_orders)

if __name__ == '__main__':
    app.run(debug=True)