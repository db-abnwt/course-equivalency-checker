from flask import Flask
import yaml

config = yaml.load(open("config.yaml", "r"), yaml.Loader)


def create_app():
    inner_config = yaml.load(open("config.yaml", "r"), yaml.Loader)
    flask = Flask(__name__, instance_relative_config=True)

    with flask.app_context():
        from icabroad.routes.routes import routes, mysql

        flask.register_blueprint(routes)

        flask.config["MYSQL_DATABASE_HOST"] = inner_config["mysql_host"]
        flask.config["MYSQL_DATABASE_USER"] = inner_config["mysql_user"]
        flask.config["MYSQL_DATABASE_PASSWORD"] = inner_config["mysql_password"]
        flask.config["MYSQL_DATABASE_DB"] = inner_config["mysql_db"]

        init_mysql = mysql
        init_mysql.init_app(flask)

        return flask


current_app = create_app()

if __name__ == "__main__":
    current_app.run(host=config.get("target_ip"), debug=True)
