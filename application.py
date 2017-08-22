from flask import Flask

app = Flask(__name__)


# Home Page
@app.route('/')
@app.route('/catalog')
def show_categories():
    return "Show Category"


# Category Items
@app.route('/catalog/<int:category_id>')
@app.route('/catalog/<int:category_id>/items')
def show_items(category_id):
    return "Show Items"


# Operations on Category
# Add Category
@app.route('/catalog/add')
def add_category():
    return "Add category"


# Edit Category
@app.route('/catalog/<int:category_id>/edit')
def edit_category(category_id):
    return "Edit category"


# Delete Category
@app.route('/catalog/<int:category_id>/delete')
def delete_category(category_id):
    return "Delete category"


# Operations on Item
# Add Item
@app.route('/catalog/<int:category_id>/add')
def add_item(category_id):
    return "Add Item"


# Edit Item
@app.route('/catalog/<int:category_id>/item/<int:item_id>/edit')
def edit_item(item_id):
    return "Edit Item"


# Delete Item
@app.route('/catalog/<int:category_id>/item/<int:item_id>/delete')
def delete_item(item_id):
    return "Delete Item"


# Login
@app.route('/login')
def login():
    return "Login Page"


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
