from flask import Flask
from flaskext.mysql import MySQL
import yaml


def create_app():
    flask = Flask(__name__, instance_relative_config=True)

    with flask.app_context():
        from routes import routes

        creds = yaml.load(open("config.yaml", "r"), yaml.Loader)
        flask.config["MYSQL_DATABASE_HOST"] = creds["mysql_host"]
        flask.config["MYSQL_DATABASE_USER"] = creds["mysql_user"]
        flask.config["MYSQL_DATABASE_PASSWORD"] = creds["mysql_password"]
        flask.config["MYSQL_DATABASE_DB"] = creds["mysql_db"]

        mysql = MySQL()
        mysql.init_app(flask)

        return flask


if __name__ == "__main__":
    current_app = create_app()
    current_app.run()
