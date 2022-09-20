from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_envvar('APP_CONFIG_FILE')

    from app.views import auth_view, main_view, order_view, test_veiw
    app.register_blueprint(main_view.bp)
    app.register_blueprint(auth_view.bp)
    app.register_blueprint(order_view.bp)
    app.register_blueprint(test_veiw.bp)

    return app


