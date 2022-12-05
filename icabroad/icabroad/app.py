from flask import Flask


def create_app():
    flask = Flask(__name__, instance_relative_config=True)

    with flask.app_context():
        from routes import routes
        return flask


if __name__ == "__main__":
    current_app = create_app()
    current_app.run()
