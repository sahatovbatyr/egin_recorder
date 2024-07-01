from flask import Blueprint, request
from schemas.user_schemas import UserCreateDto

from schemas.auth_schemas import AuthRequestDto
from services.auth_service import AuthService

auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/api/auth/register', methods=['POST'])
def register_user():
    """
    Регистрация нового пользователя
    POST /api/auth/register
    """
    data = request.get_json()
    schema = UserCreateDto()
    errors = schema.validate(data)
    if errors:
        return {'message': 'Ошибка валидации', 'errors': errors}, 400

    return AuthService.register_user(data)


@auth_bp.route('/api/auth/login', methods=['POST'])
def login_user():
    """
    Аутентификация пользователя
    POST /api/auth/login
    """
    user_data = request.get_json()
    userSchema = AuthRequestDto()
    errors = userSchema.validate(user_data)

    if errors:
        return {'message': 'Validation error', 'errors': errors}, 400

    return AuthService.authenticate_user(userSchema)
