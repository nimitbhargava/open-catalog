from flask import Flask, render_template, url_for, request, redirect, jsonify, session as login_session, make_response
from sqlalchemy import create_engine
from database_setup import Base, User, Category, Item
from sqlalchemy.orm import sessionmaker
from config import GOOGLE_CLIENT_ID
import random, string, json, httplib2, requests
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError

app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']

# Connect to database opencatalog.db
engine = create_engine('sqlite:///opencatalog.db')
Base.metadata.bind = engine

# Create database session
DBSession = sessionmaker(bind=engine)
session = DBSession()


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session['email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


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
    # Create anti-forgery state token
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state, client_id=GOOGLE_CLIENT_ID)


# Logout
@app.route('/logout')
def logout():
    if login_session['provider'] == 'google':
        gdisconnect()
        del login_session['gplus_id']
        del login_session['access_token']
    del login_session['username']
    del login_session['email']
    del login_session['user_id']
    del login_session['provider']
    return redirect(url_for('show_categories'))


# Google Login
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate Anti-Forgery State Token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Token's client ID does not match app's."), 401)
        print
        "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')

    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'

    # See if user exists
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    return "Login Successful"


# Google Logout
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')

    if access_token is None:
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


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
    app.secret_key = 'ultra_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
