from flask import Flask, render_template, url_for, request, redirect, jsonify
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
    category = categories.filter_by(id=category_id).first()
    items_of_category = session.query(Item).filter_by(category_id=category_id).all()
    return render_template('items.html', categories=all_categories, items=items_of_category,
                           category=category)


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
    category = session.query(Category).filter_by(id=(item.category_id)).first()
    return render_template('item.html', item=item, category=category)


# Operations on Item
# Add Item
@app.route('/catalog/<int:category_id>/add', methods=['GET', 'POST'])
@app.route('/catalog/<int:category_id>/item/add', methods=['GET', 'POST'])
def add_item(category_id):
    category = session.query(Category).filter_by(id=category_id).first()
    if category is None:
        return "Incorrect request"
    if request.method == 'POST':
        newItem = Item(title=request.form['title'], description=request.form['description'], category_id=category_id,
                       owner_id=1)
        session.add(newItem)
        session.commit()
        return redirect(url_for('show_items', category_id=category_id))
    return render_template('add_item.html', category=category)


# Edit Item
@app.route('/catalog/<int:category_id>/item/<int:item_id>/edit', methods=['GET', 'POST'])
def edit_item(category_id, item_id):
    editItem = session.query(Item).filter_by(id=item_id, category_id=category_id).first()
    if editItem is None:
        return "Incorrect request"
    if request.method == 'POST':
        editItem.title = request.form['title'] if request.form['title'] else editItem.title
        editItem.description = request.form['description'] if request.form['description'] else editItem.description
        session.add(editItem)
        session.commit()
        return redirect(url_for('view_item', category_id=category_id, item_id=editItem.id))
    category = session.query(Category).filter_by(id=category_id).first()
    return render_template('edit_item.html', item=editItem, category=category)


# Delete Item
@app.route('/catalog/<int:category_id>/item/<int:item_id>/delete', methods=['GET', 'POST'])
def delete_item(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id, category_id=category_id).first()
    if item is None:
        return "Incorrect request"
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        return redirect(url_for('show_items', category_id=category_id))
    category = session.query(Category).filter_by(id=category_id).first()
    return render_template('delete_item.html', item=item, category=category)


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


# APIs
# Return with all the categories
@app.route('/catalog/JSON')
def returnAllCategories():
    categories = session.query(Category).all()
    return jsonify(categories=[category.serialize for category in categories])


# Return with all the items of a specific category
@app.route('/catalog/<int:category_id>/JSON')
def returnAllItemsofCategory(category_id):
    items = session.query(Item).filter_by(category_id=category_id).all()
    if items is None:
        return "Incorrect request"
    return jsonify(items=[item.serialize for item in items])


# Return with all the details of an item
@app.route('/catalog/<int:category_id>/item/<int:item_id>/JSON')
def returnItem(category_id, item_id):
    item = session.query(Item).filter_by(category_id=category_id, id=item_id)
    if item is None:
        return "Incorrect request"
    return jsonify(items=[item.serialize for item in item])


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
