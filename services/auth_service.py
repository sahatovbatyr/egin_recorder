from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, UserRole
from schemas.auth_schemas import AuthRequestDto
from schemas.user_schemas import UserCreateDto
from datetime import timedelta
from sqlalchemy.exc import IntegrityError

class AuthService:

    @staticmethod
    def register_user(user_data: UserCreateDto):

        new_user = User(username=user_data.username,
                        password=generate_password_hash(user_data.password))

        default_role = UserRole.query.filter_by(title='USER').first()
        if default_role:
            new_user.roles.append(default_role)

        try:
            db.session.add(new_user)
            db.session.commit()
            return {'message': 'Пользователь успешно зарегистрирован'}, 201
        except IntegrityError:
            db.session.rollback()
            return {'message': 'Пользователь с таким именем уже существует'}, 400

    @staticmethod
    def authenticate_user(authRequestDto: AuthRequestDto):
        username = authRequestDto.username
        password = authRequestDto.password
        user:User = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            access_token = create_access_token(
                identity=user.id,
                expires_delta=timedelta(days=1)
            )

            refresh_token = create_refresh_token( identity=user.id )

            return {'access_token': access_token, 'refresh_token': refresh_token}, 200
        else:
            return {'message': 'Неверные учетные данные'}, 401
