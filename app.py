from flask import Flask
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from models import db
import os

from flask_sqlalchemy import SQLAlchemy

# Load environment variables
load_dotenv()
app = Flask(__name__)
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DATABASE = os.getenv("DATABASE")
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DATABASE}"

db.init_app(app)
# JWT setup
jwt = JWTManager(app)

# Import blueprints
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.task_routes import task_bp

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(task_bp)

# Создание всех таблиц в базе данных
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
