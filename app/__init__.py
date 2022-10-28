from flask import Flask
import pymysql
def db_connection():
    db = pymysql.connect(host='localhost', port=3306, user='dbuser', passwd='!miryangUTIL2022',db='UTILITY_SERVICE', charset='utf8')
    return db


def create_app():
    app = Flask(__name__)
    app.config.from_envvar('APP_CONFIG_FILE')

    from app.views import auth_view, main_view, order_view, admin_veiw, taxi_view
    app.register_blueprint(main_view.bp)
    app.register_blueprint(auth_view.bp)
    app.register_blueprint(order_view.bp)
    app.register_blueprint(admin_veiw.bp)
    app.register_blueprint(taxi_view.bp)

    return app


