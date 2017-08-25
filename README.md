## Open Catalog
A web application that provides a list of items within a variety of categories and integrate third party user registration and authentication. 

Authenticated users have the ability to post, edit, and delete their own items.

### Steps to run

1. Install Vagrant and VirtualBox
2. Clone the [Vagrant Environment](https://github.com/udacity/fullstack-nanodegree-vm)
3. Launch the Vagrant VM (`vagrant up`)
4. Run `python lotsofcategoryanditem.py` to seed database 
5. Run `application.py`
6. Access the application by visiting http://localhost:8000 locally

### JSON End Points

- [Return with all the categories](http://localhost:8000/catalog/JSON)
- [Return with all the items of a specific category](http://localhost:8000/catalog/1/JSON)
- [eturn with all the details of an item](http://localhost:8000/catalog/1/item/1/JSON)

### Steps to add a new item

1. Go to category page
2. Click on Add Item button. If not logged in you will be redirected to login page 
3. Enter the title and description of item and click on save

### Steps to edit an item

1. Go to category page
2. Click on the item from the list. If not logged in you will be redirected to login page 
3. Update the title and description of item and click on save

### Steps to delete an item

1. Go to category page
2. Click on the item you want to delete
3. Click on the delete option available after the item description