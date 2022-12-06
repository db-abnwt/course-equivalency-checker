from flask import Flask
import yaml

config = yaml.load(open("config.yaml", "r"), yaml.Loader)


def create_app():
    flask = Flask(__name__, instance_relative_config=True)

    with flask.app_context():
        from routes import routes

        flask.config["MYSQL_DATABASE_HOST"] = config["mysql_host"]
        flask.config["MYSQL_DATABASE_USER"] = config["mysql_user"]
        flask.config["MYSQL_DATABASE_PASSWORD"] = config["mysql_password"]
        flask.config["MYSQL_DATABASE_DB"] = config["mysql_db"]

        init_mysql = routes.mysql
        init_mysql.init_app(flask)

        return flask


if __name__ == "__main__":
    current_app = create_app()
    current_app.run(host=config.get("target_ip"), debug=True)
