import sqlite3
import click
from flask import current_app, g

def init_app(app):
    # tells Flask to call that function when cleaning up after returning the response.
    app.teardown_appcontext(close_db)
    # adds a new command that can be called with flask command.
    app.cli.add_command(init_db_command)

def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def get_db():
    # `g` is a special object that is unique for each request.
    # It is used to store data that might be accessed by multiple
    # fuctions during the request.
    
    # The connection is stored and reused instead of creating a new 
    # connection if get_db is called a second time in the same request.
    if 'db' not in g:
        # `sqlites3.connect()` establishs a connection to the file pointed at by the `DATABASE`
        # configuration key. This file doesn't have to exist yet, and won't
        # until you initialize the database later
        g.db = sqlite3.connect(
            # current_app is another special object hat points the Flask application
            # handling the request.

            # Since you used an application factory, there is no application object
            # when write the rests of you code.
            # `get_db` will be called when the application has been created
            # and is handling a request, so `current_app` can be used
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        
        # sqlite3.Row tells the connection to return rows that behave like dicts
        # This allows accessing the column by names
        g.db.row_factory = sqlite3.Row
    return g.db

# `close_db` checks if a connection was created by checking if `db` was set
# If the connection exsits, it is closed
def close_db(e=None):
    db = g.pop('db', None)
    
    if db is not None:
        db.close()

