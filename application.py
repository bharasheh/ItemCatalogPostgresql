#!/usr/bin/env python2
#
# Item Catalog Project that allows the user to browse, add, edit, and delete
# catalog categories and items. It uses integration with Google API for login
# and authorisation to allow users edit or delete their data only, in
# addition to REST end-point to view the data. The project is using
# database to store all information.

from flask import (Flask, render_template, request, redirect, url_for, flash,
                   jsonify, abort, g, make_response)
from flask import session as flask_session
from flask_httpauth import HTTPBasicAuth
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, CategoryItem
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import requests
import json

app = Flask(__name__)

engine = create_engine("postgresql://catalog:catalog@localhost:5432/catalog")
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

auth = HTTPBasicAuth()

CLIENT_ID = json.loads(open('/var/www/ItemCatalog/client_secrets.json', 'r')
                       .read())['web']['client_id']


def verify_user():
    """Verify the user is logged in to the system"""
    if 'logged_in' in flask_session:
        return True
    return False


@app.route('/')
def showCategories():
    """Show all categories in the system"""
    categories = session.query(Category).all()
    latest_items = session.query(CategoryItem).order_by(
                                 CategoryItem.id.desc()).limit(9)
    return render_template('categories.html', categories=categories,
                           latest_items=latest_items)


@app.route('/catalog/<string:category_name>/items')
def showCategoryItems(category_name):
    """Show all category items for the given category"""
    category = session.query(Category).filter_by(name=category_name).one()
    category_items = session.query(CategoryItem).filter_by(
                                   category_id=category.id).all()
    category_items_count = len(category_items)
    return render_template('categoryItems.html', category=category,
                           category_items=category_items,
                           category_items_count=category_items_count)


@app.route('/catalog/<string:category_name>/<string:category_item_title>')
def showCategoryItem(category_name, category_item_title):
    """Show category item details for the given category and category item"""
    category = session.query(Category).filter_by(name=category_name).one()
    category_item = session.query(CategoryItem).filter_by(
                                  category_id=category.id,
                                  title=category_item_title).one()
    return render_template('categoryItem.html', category_item=category_item)


@app.route('/catalog/new', methods=['GET', 'POST'])
def newCategoryItem():
    """New category item page and insert the new item in the database"""
    if not verify_user():
        return render_template('noAccess.html')
    if request.method == 'POST':
        newCategoryItem = CategoryItem(title=request.form['title'],
                                       description=request.form['description'],
                                       category_id=request.form['category_id'],
                                       user_id=flask_session['user_id'])
        session.add(newCategoryItem)
        session.commit()
        flash("New Category Item Created")
        category = session.query(Category).filter_by(
                                 id=newCategoryItem.category_id).one()
        return redirect(url_for('showCategoryItems',
                        category_name=category.name))
    else:
        categories = session.query(Category).all()
        return render_template('newCategoryItem.html', categories=categories)


@app.route('/catalog/<string:category_item_title>/edit',
           methods=['GET', 'POST'])
def editCategoryItem(category_item_title):
    """Edit category item page and update the edited item in the database"""
    if not verify_user():
        return render_template('noAccess.html')
    categoryItemToEdit = session.query(CategoryItem).filter_by(
                                       title=category_item_title).one()
    if categoryItemToEdit.user_id != flask_session['user_id']:
        return render_template('noAccess.html')
    if request.method == 'POST':
        if request.form['title']:
            categoryItemToEdit.title = request.form['title']
        if request.form['description']:
            categoryItemToEdit.description = request.form['description']
        if request.form['category_id']:
            categoryItemToEdit.category_id = request.form['category_id']
        session.add(categoryItemToEdit)
        session.commit()
        flash("Category Item Successfully Edited")
        category = session.query(Category).filter_by(
                                 id=categoryItemToEdit.category_id).one()
        return redirect(url_for('showCategoryItem',
                        category_name=category.name,
                        category_item_title=categoryItemToEdit.title))
    else:
        categories = session.query(Category).all()
        return render_template('editCategoryItem.html',
                               categoryItem=categoryItemToEdit,
                               categories=categories)


@app.route('/catalog/<string:category_item_title>/delete',
           methods=['GET', 'POST'])
def deleteCategoryItem(category_item_title):
    """Delete category item page and delete the item from the database"""
    if not verify_user():
        return render_template('noAccess.html')
    categoryItemToDelete = session.query(CategoryItem).filter_by(
                                         title=category_item_title).one()
    if categoryItemToDelete.user_id != flask_session['user_id']:
        return render_template('noAccess.html')
    if request.method == 'POST':
        session.delete(categoryItemToDelete)
        session.commit()
        flash("Category Item Successfully Deleted")
        category = session.query(Category).filter_by(
                                 id=categoryItemToDelete.category_id).one()
        return redirect(url_for('showCategoryItems',
                        category_name=category.name))
    else:
        return render_template('deleteCategoryItem.html',
                               categoryItemToDelete=categoryItemToDelete)


# API Endpoints
@app.route('/catalog.json')
def showCategoriesJSON():
    """REST end-point to show all categories with category items"""
    categories = session.query(Category).all()
    return jsonify(Category=[category.serialize for category in categories])


@app.route('/catalog.json/<string:category_name>/<string:category_item_title>')
def showCategoryItemJSON(category_name, category_item_title):
    """REST end-point to show a category item"""
    category = session.query(Category).filter_by(name=category_name).one()
    categoryItem = session.query(CategoryItem).filter_by(
                                  category_id=category.id,
                                  title=category_item_title).one()
    return jsonify(CategoryItem=[categoryItem.serialize])


@app.route('/oauth/<provider>', methods=['POST'])
def login(provider):
    """Login to the system using third party provider (Google)"""
    # STEP 1 - Parse the auth code
    # auth_code = request.json.get('auth_code')
    auth_code = request.data
    print "Step 1 - Complete, received auth code %s" % auth_code
    if provider == 'google':
        # STEP 2 - Exchange for a token
        try:
            # Upgrade the authorization code into a credentials object
            oauth_flow = flow_from_clientsecrets('client_secrets.json',
                                                 scope='')
            oauth_flow.redirect_uri = 'postmessage'
            credentials = oauth_flow.step2_exchange(auth_code)
        except FlowExchangeError:
            response = make_response(json.dumps('Failed to upgrade the '
                                     + 'authorization code.'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        # Check that the access token is valid.
        access_token = credentials.access_token
        url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
               % access_token)
        h = httplib2.Http()
        result = json.loads(h.request(url, 'GET')[1])
        # If there was an error in the access token info, abort.
        if result.get('error') is not None:
            response = make_response(json.dumps(result.get('error')), 500)
            response.headers['Content-Type'] = 'application/json'

        print "Step 2 Complete! Access Token : %s " % credentials.access_token

        # STEP 3 - Find User or make a new one

        # Get user info
        h = httplib2.Http()
        userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        params = {'access_token': credentials.access_token, 'alt': 'json'}
        answer = requests.get(userinfo_url, params=params)

        data = answer.json()

        name = data['name']
        picture = data['picture']
        email = data['email']

        # See if user exists, if it doesn't make a new one
        user = session.query(User).filter_by(email=email).first()
        if not user:
            user = User(username=name, picture=picture, email=email)
            session.add(user)
            session.commit()

        # STEP 4 - Make token
        token = user.generate_auth_token(600)

        flask_session['user_id'] = user.id
        flask_session['username'] = user.username
        flask_session['email'] = user.email
        flask_session['logged_in'] = True

        # STEP 5 - Send back token to the client
        return jsonify({'token': token.decode('ascii')})
    else:
        return 'Unrecoginized Provider'


@app.route('/logout')
def logout():
    """Logout from the third party provider (Google)"""
    flask_session.pop('username', None)
    flask_session.pop('email', None)
    flask_session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('showCategories'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=80)
