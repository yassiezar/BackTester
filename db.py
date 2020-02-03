import sqlalchemy as db

from sqlalchemy_utils import database_exists, create_database

DB_TYPE = 'sqlite'
DB_USER = 'jaycee'
DB_PASSWORD = 'jaycee'
DB_HOST = 'localhost'
DB_NAME = 'db.db'

if DB_TYPE == 'sqlite':
    engine = db.create_engine('{}:///{}'.format(DB_TYPE, DB_NAME))
elif DB_TYPE == 'mysql':
    engine = db.create_engine('{}://{}:{}@{}/{}'.format(DB_TYPE, DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)),

if not database_exists(engine.url):
    create_database(engine.url)
print(database_exists(engine.url))
