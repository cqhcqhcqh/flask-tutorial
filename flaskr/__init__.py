import os
from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    # __name__ is the name of the current Python module
    # __name__ let app knows where it's located to set up some path
    # and __name__ is a convenient way to tell it that.

    # instance_relative_config=True
    # tells the app the configuration files are relative to 
    # the `instance folder`
    # The instance folder is located outsider the `flaskr` package
    # and can hold local data that shouldn't be committed to version
    # control, sunch as configuration secrets and the database file
    print("current module name is %s"%(__name__))
    app = Flask(__name__, instance_relative_config=True)

    # sets some default configuration that the app will use
    app.config.from_mapping(
        # SECRET_KEY is used by Flask and extensions to keep data safe
        # set to `dev` to provider a convenient value during the devlopment
        # it should be overridden with a random value when deploying
        SECRET_KEY='dev',
        # `DATABASE` is the path where the SQLite database file will be saved.
        # It's under `app.instance_path`, which is the path that Flask has chosen for
        # instance folder.
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )

    if test_config is None:
        # `app.config.from_pyfile()` override the default configuration with values taken from
        # `config.py`` file in the `instance folder` if it exist.
        # For example, when deploying, this can be used to set a real `SECRET_KEY`

        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # `test_config` can also be passed to the factory, and will be used instead of the instance
        # configuration. This is so the tests you'll write later in the tutorial can be configured 
        # independently of any development values you have configured.

        # load the test config if passed in
        app.config.from_mapping(test_config)
    
    # ensure the instance folder exists
    # Flask doesn't create the instance folder automatically, but it needs to be 
    # created because will create the SQLite database file there.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # `@app.router` create a simple route so you can see the application working
    # before getting into the rest of the tutorial.
    # It creats a connection between the URL/hello and a function that returns a response
    # the string 'Hello world!' in this case.
    
    # Python 中的装饰器语法
    # a simple page that says heelo
    @app.route('/hello')
    def hello():
        return 'hello, world!'
    
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
    return app