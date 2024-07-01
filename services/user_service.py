from functools import wraps
from typing import List

from flask_jwt_extended import get_jwt_identity

from exceptions import UserNotFoundException, UserExistsException, AccessDeniedException
from models import db, User, UserRole
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from schemas.user_schemas import UserCreateDto, UserDto, UserChangePasswordDto


class UserService:

    @staticmethod
    def admin_required(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            current_user_id = get_jwt_identity()
            user_roles: List[UserRole] = UserService.get_user_roles(current_user_id)

            if 'ADMIN' not in user_roles:
                return {'message': 'Доступ запрещен. Требуется роль ADMIN'}, 403

            return fn(*args, **kwargs)

        return wrapper

    @staticmethod
    @admin_required
    def create_user(userCreateDTO: UserCreateDto):
        new_user = User(
            username=userCreateDTO.username,
            password=generate_password_hash(userCreateDTO.password))

        if userCreateDTO.password != userCreateDTO.passwordConfirmation:
            return {'message': 'Пользователь с таким именем уже существует'}, 400

        default_role = UserRole.query.filter_by(title='USER').first()
        if default_role:
            new_user.roles.append(default_role)

        try:
            db.session.add(new_user)
            db.session.commit()
            return {'message': 'Пользователь успешно создан'}, 201
        except IntegrityError:
            db.session.rollback()
            raise UserExistsException(userCreateDTO.username)

    @staticmethod
    def update_user_password(userDto: UserChangePasswordDto):

        if userDto.password != userDto.passwordConfirmation:
            raise AccessDeniedException("Passwords are not match.")

        current_user_id = get_jwt_identity()
        if current_user_id != userDto.id:
            return {'message': 'Вы можете изменить только свой пароль'}, 403

        user: User = UserService.getById_user(userDto.id)

        if not check_password_hash(user.password, userDto.password):
            raise AccessDeniedException("Username or Passwords are not match.")

        user.password = generate_password_hash(userDto.password)

        try:
            db.session.commit()
            return {'message': 'Пароль успешно изменен'}, 200
        except IntegrityError:
            db.session.rollback()
            return {'message': 'Ошибка изменения пароля'}, 400

    # @staticmethod
    # def update_user(user_id, user_data: UserUpdateDTO):
    #     user = User.query.get(user_id)
    #     user.username = user_data.username
    #     if user_data.is_active is not None:
    #         user.is_active = user_data.is_active
    #
    #     try:
    #         db.session.commit()
    #         return {'message': 'Информация о пользователе успешно обновлена'}, 200
    #     except IntegrityError:
    #         db.session.rollback()
    #         return {'message': 'Ошибка обновления информации о пользователе'}, 400

    @staticmethod
    @admin_required
    def set_user_active_status(userDto: UserDto):
        user = UserService.getById_user(userDto.id)
        user.is_active = userDto.is_active

        try:
            db.session.commit()
            return {'message': 'Статус активности пользователя успешно изменен'}, 200
        except IntegrityError:
            db.session.rollback()
            return {'message': 'Ошибка изменения статуса активности пользователя'}, 400

    @staticmethod
    @admin_required
    def delete_user(user_id):
        user = UserService.getById_user(user_id)

        try:
            db.session.delete(user)
            db.session.commit()
            return {'message': 'Пользователь успешно удален'}, 200
        except IntegrityError:
            db.session.rollback()
            return {'message': 'Ошибка удаления пользователя'}, 400

    @staticmethod
    def getById_user(user_id: int) -> User:
        user = User.query.get(user_id)
        if user == None:
            raise UserNotFoundException(user_id)
        return user

    @staticmethod
    def get_user_roles(user_id: int) -> List[UserRole]:
        user: User = User.query.get(user_id)
        if user == None:
            raise UserNotFoundException(user_id)
        return user.roles

    @staticmethod
    def update_user_roles(user_id, roles: list):
        user = UserService.getById_user(user_id)
        roles_to_assign = UserRole.query.filter(UserRole.title.in_(roles)).all()
        user.roles = roles_to_assign

        try:
            db.session.commit()
            return {'message': 'Роли пользователя успешно обновлены'}, 200
        except IntegrityError:
            db.session.rollback()
            return {'message': 'Ошибка обновления ролей пользователя'}, 400
