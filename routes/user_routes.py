from functools import wraps
from typing import List

from flask import Blueprint, request

from models import UserRole
from schemas.user_schemas import UserCreateDto, UserChangePasswordDto,  UserDto
from services.user_service import UserService
from flask_jwt_extended import jwt_required

user_bp = Blueprint('user_bp', __name__)


# Маршрут для создания нового пользователя

@user_bp.route('/api/user/test', methods=['GET'])
def test_connect():
    return {'message': 'Sucess'}, 201

@user_bp.route('/api/user/create', methods=['POST'])
@jwt_required()
@UserService.admin_required
def create_user():

    user_data = request.get_json()
    userschema = UserCreateDto()
    errors = userschema.validate(user_data)
    if errors:
        return {'message': 'Validation error', 'errors': errors}, 400

    UserService.create_user(userschema)
    return {'message': 'Пользователь успешно создан'}, 201

# Маршрут для изменения пароля пользователя
@user_bp.route('/api/user/update-password', methods=['POST'])
@jwt_required()
def update_password():

    user_data = request.get_json()
    userSchema = UserChangePasswordDto()
    errors = userSchema.validate(user_data)

    if errors:
        return {'message': 'Validation error', 'errors': errors}, 400

    UserService.update_user_password(userSchema)
    return {'message': 'Пароль успешно изменен'}, 200

# Маршрут для изменения статуса активности пользователя
@user_bp.route('/api/user/set-active', methods=['PATCH'])
@jwt_required()
def set_active():

    user_data = request.get_json()
    userSchema = UserDto()
    errors = userSchema.validate(user_data)

    if errors:
        return {'message': 'Validation error', 'errors': errors}, 400

    UserService.set_user_active_status(userSchema)

    return {'message': 'успешно изменен'}, 200

# Маршрут для удаления пользователя
@user_bp.route('/api/user/delete/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):

    UserService.delete_user(user_id)
    return {'message': 'Пользователь успешно удален'}, 200

# Маршрут для изменения ролей пользователя
@user_bp.route('/api/user/change-roles/<int:user_id>', methods=['PATCH'])
@jwt_required()
def change_roles(user_id):
    # user_data = request.get_json()
    # userDto = UserDto(id=user_id, roles=user_data['roles'])
    # UserService.update_user(userDto)
    return {'message': 'Роли пользователя успешно изменены'}, 200
