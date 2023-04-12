from flask_sqlalchemy import SQLAlchemy


#   cREO UN OBJETO SQLALCHEMY DESDE LA extension de flask_sqlalchemy
# y así podemos vincuilarlo a niuestra aplicacion   
db = SQLAlchemy()


"""
db.py
---
Later on, this file will be replaced by SQLAlchemy. For now, it mimics a database.
Our data storage is:
    - stores have a unique ID and a name
    - items have a unique ID, a name, a price, and a store ID.
"""

stores = {}
items = {}