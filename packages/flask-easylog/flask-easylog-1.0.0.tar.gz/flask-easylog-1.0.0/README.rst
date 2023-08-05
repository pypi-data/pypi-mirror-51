Flask-easylog
=============

help log management for flask application


Installation
------------

::

    pip install flask-easylog
        
Or

::

    git clone https://github.com/fraoustin/flask-easylog.git
    cd flask-easylog
    python setup.py install

You can load test by

::

    python -m unittest discover -s test

Usage
-----

::

    from flask import Flask, request, current_app
    from logging import DEBUG, INFO, ERROR

    from flask_easylog import EasyLog, FMT_ACCESS_LOG, log, SpecificLevelLog, Api, Ui 

    app = Flask(__name__)
    app.secret_key = 'super secret string'
    app.logger.setLevel(INFO)

    app.logger.info("before add EasyLog")

    EasyLog(app,
        fmt = FMT_ACCESS_LOG,
        afterlog = True,
        beforelog = True)
    app.register_blueprint(Api(url_prefix='/api'))
    app.register_blueprint(Ui(url_prefix='/ui'))
    app.logger.info("after add EasyLog")

    @app.route("/")
    def hello():
        current_app.logger.critical("critical from hello")
        current_app.logger.error("error from hello")
        current_app.logger.info("info from hello")
        current_app.logger.debug("debug from hello")
        return "Hello World!"

    @app.route("/one")
    @log(DEBUG)
    def one():
        current_app.logger.critical("critical from one")
        current_app.logger.error("error from one")
        current_app.logger.info("info from one")
        current_app.logger.debug("debug from one")
        return "Hello World!"

    @app.route("/two")
    @log
    def two():
        current_app.logger.critical("critical from two")
        current_app.logger.error("error from two")
        current_app.logger.info("info from two")
        current_app.logger.debug("debug from two")
        return "Hello World!"

    @app.route("/three")
    @log(ERROR)
    def three():
        current_app.logger.critical("critical from three")
        current_app.logger.error("error from three")
        current_app.logger.info("info from three")
        current_app.logger.debug("debug from three")
        return "Hello World!"

    @app.route("/four")
    def four():
        current_app.logger.critical("critical from four")
        current_app.logger.error("error from four")
        current_app.logger.info("info from four")
        current_app.logger.debug("debug from four")
        return "Hello World!"

    SpecificLevelLog['four']=ERROR

    if __name__ == "__main__":
        app.logger.info("before run")
        app.run(host="0.0.0.0", port=8080)

Documentation
-------------

`Plugin EasyLog <https://github.com/fraoustin/flask-easylog/tree/master/doc/plugin.rst>`_

`Api EasyLog <https://github.com/fraoustin/flask-easylog/tree/master/doc/api.rst>`_

`Ui EasyLog <https://github.com/fraoustin/flask-easylog/tree/master/doc/ui.rst>`_