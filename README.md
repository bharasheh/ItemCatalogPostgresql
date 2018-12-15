# Item Catalog

Source code for Item Catalog project.

Please follow below steps to run the application:

## Requirements

You need to have git and any browser installed.

## Download the source code

Use git to [clone](https://services.github.com/on-demand/github-cli/clone-repo-cli) or download the source code from https://github.com/bharasheh/ItemCatalog.git

Install the requirements for the code by run the command ```$ env2/bin/pip install -r requirements.txt```

## Database Setup

The database file ```itemcatalog.db``` is provided with the code with testing data, but you can delete this file and run ```python database_setup.py``` to create new empty database file, and run ```python insert_data.py``` to insert the testing data.

## Google Account

You need to have Google account to login to the system.

## Run the Application

Start the application using the command ```python application.py```

## Open the web site
Open the url http://localhost:8000 using any browser.

## REST End-Points
The below JSON rest points are available in the system:
1) Get list of all categories with category items http://localhost:8000/catalog.json
2) Get a category item details http://localhost:8000/catalog.json/<string:category_name>/<string:category_item_title> e.g. http://localhost:8000/catalog.json/Soccer/Liverpool
