from flask import Flask, render_template
from sqlalchemy import create_engine
from database_setup import Base, User, Category, Item
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# Connect to database opencatalog.db
engine = create_engine('sqlite:///opencatalog.db')
Base.metadata.bind = engine

# Create database session
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Home Page
@app.route('/')
@app.route('/catalog')
def show_categories():
    categories = session.query(Category).all()
    latest_5_items = session.query(Item).all()
    return render_template('categories.html', categories=categories, items=latest_5_items)


# Category Items
@app.route('/catalog/<int:category_id>')
@app.route('/catalog/<int:category_id>/items')
def show_items(category_id):
    categories = session.query(Category)
    all_categories = categories.all()
    category_name = categories.filter_by(id=category_id).first().name
    items_of_category = session.query(Item).filter_by(category_id=category_id).all()
    return render_template('items.html', categories=all_categories, items=items_of_category,
                           category_name=category_name)


# Operations on Category
# Add Category
@app.route('/catalog/add')
def add_category():
    return render_template('add_category.html')


# Edit Category
@app.route('/catalog/<int:category_id>/edit')
def edit_category(category_id):
    return render_template('edit_category.html')


# Delete Category
@app.route('/catalog/<int:category_id>/delete')
def delete_category(category_id):
    return render_template('delete_category.html')


# View Item
@app.route('/catalog/<int:category_id>/item/<int:item_id>')
def view_item(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).first()
    category_name = session.query(Category).filter_by(id=(item.category_id)).first().name
    return render_template('item.html', item=item, category_name=category_name)


# Operations on Item
# Add Item
@app.route('/catalog/<int:category_id>/add')
@app.route('/catalog/<int:category_id>/item/add')
def add_item(category_id):
    category = session.query(Category).filter_by(id=category_id).first()
    if category is None:
        return "Incorrect request"
    return render_template('add_item.html', category=category)


# Edit Item
@app.route('/catalog/<int:category_id>/item/<int:item_id>/edit')
def edit_item(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id, category_id=category_id).first()
    if item is None:
        return "Incorrect request"
    return render_template('edit_item.html', item=item)


# Delete Item
@app.route('/catalog/<int:category_id>/item/<int:item_id>/delete')
def delete_item(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id, category_id=category_id).first()
    if item is None:
        return "Incorrect request"
    return render_template('delete_item.html', item=item)


# Login
@app.route('/login')
def login():
    return render_template('login.html')


# Logout
@app.route('/login')
def logout():
    return "Logout Page"


# Google Login
@app.route('/gconnect')
def gconnect():
    return "gconnect"


# Google Logout
@app.route('/gdisconnect')
def gdisconnect():
    return "g disconnect Page"


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
