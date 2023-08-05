import logging
import os

from pathlib import Path
from pkg_resources import get_distribution, DistributionNotFound

import click

from flask import Flask, current_app
from flask_restful import Api

from .directory_monitoring import DirectoryMonitoring
from .resources import Mount, SupportedLibraries
from .utils import init_db, monitor_image_dir
from .views import main


try:
    __version__ = get_distribution('thumbtack').version
except DistributionNotFound:
    __version__ = 'Could not find version'


def create_app(image_dir=None, database=None):
    app = Flask(__name__)
    app.config.from_object('thumbtack.config')

    if os.environ.get("MOUNT_DIR"):
        app.config.update(MOUNT_DIR=os.environ.get("MOUNT_DIR"))

    # priority goes to command line args, then env variables, then val from config.py
    if image_dir:
        app.config.update(IMAGE_DIR=image_dir)
    elif os.environ.get("IMAGE_DIR"):
        app.config.update(IMAGE_DIR=os.environ.get("IMAGE_DIR"))

    if database:
        app.config.update(DATABASE=database)
    elif os.environ.get("DATABASE"):
        app.config.update(DATABASE=os.environ.get("DATABASE"))

    configure(app)

    app.before_first_request(before_first_request)

    return app


def configure(app):
    configure_extensions(app)
    configure_blueprints(app)

    # WARNING!
    # At app startup, this deletes the current, local sqlite database and creates a new one.
    # this may be confusing if it didn't clean up after itself previously and images are still mounted,
    # but not tracked by a new instance of the DB.
    configure_database(app)
    app.logger.info('configured')


def configure_extensions(app):
    app.logger.info('configuring extensions')
    api = Api(app)

    api.add_resource(Mount,
                     '/mounts/<path:image_path>',
                     '/mounts/')
    api.add_resource(SupportedLibraries,
                     '/supported',
                     endpoint='supported')


def configure_blueprints(app):
    app.logger.info('configuring blueprints')
    app.register_blueprint(main)


def configure_database(app):
    db_file = Path(app.config['DATABASE'])

    with app.app_context():
        if db_file.is_file():
            db_file.unlink()

        if not db_file.is_file():
            init_db()


def before_first_request():
    configure_logging(current_app)


def configure_logging(app):
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s in %(name)s.%(module)s: %(message)s")

    if app.debug:
        app.logger.setLevel(logging.DEBUG)
    else:
        app.logger.setLevel(logging.INFO)

        # In production mode, add log handler to sys.stderr.
        shandler = logging.StreamHandler()
        shandler.setLevel(logging.INFO)
        shandler.setFormatter(formatter)
        # app.logger.addHandler(shandler)


@click.command()
@click.option('-d', '--debug', default=False, is_flag=True, help='Run the Thumbtack server in debug mode')
@click.option('-h', '--host', default='127.0.0.1',
              show_default=True, help='Host to run Thumbtack server on')
@click.option('-p', '--port', default='8208',
              show_default=True, help='Port to run Thumbtack server on')
@click.option('-i', '--image-dir',
              help='Directory of disk images for Thumbtack server to monitor  [Default: $CWD]')
@click.option('--db', 'database', help='SQLite database to store mount state')
def start_app(debug, host, port, image_dir, database):
    app = create_app(image_dir=image_dir, database=database)
    directory_monitoring_thread = DirectoryMonitoring(app)
    directory_monitoring_thread.start()
    app.run(debug=debug, host=host, port=port)
