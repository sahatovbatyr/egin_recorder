from marshmallow import Schema, fields, post_load, validates, ValidationError
# from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
# from extensions import ma
# from models import User, UserRole


class UserDto(Schema):
    id = fields.Int(required=True)
    username = fields.Str(required=True)
    is_active = fields.Bool(required=True)

class UserCreateDto(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    passwordConfirmation = fields.Str(required=True)
    roles = fields.List(fields.Str(), required=True)


class UserDeleteDto(Schema):
    id = fields.Int(required=True)
    username = fields.Str(required=True)

class UserChangePasswordDto(Schema):
    id = fields.Int(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    newPassword = fields.Str(required=True)
    passwordConfirmation = fields.Str(required=True)

class UserChangeRolesDto(Schema):
    id = fields.Int(required=True)
    roles = fields.List(fields.Str(), required=True)

class UserSetActiveDto(Schema):
    id = fields.Int(required=True)
    is_active = fields.Bool(required=True)


# class UserSchema(Schema):
#     id = fields.Int(dump_only=True)
#     username = fields.Str(required=True)
#     roles = fields.List(fields.Str)
#     is_active = fields.Bool()

# class UserCreateSchema(Schema):
#     username = fields.Str(required=True)
#     password = fields.Str(required=True)
#     roles = fields.List(fields.Str(), required=True)

# class UserUpdateSchema(Schema):
#     id = fields.Int(required=True)
#     username = fields.Str(required=True)

# class UserDeleteSchema(Schema):
#     id = fields.Int(required=True)
#     username = fields.Str(required=True)

# class UserChangePasswordSchema(Schema):
#     id = fields.Int(required=True)
#     password = fields.Str(required=True)

# class UserChangeRolesSchema(Schema):
#     id = fields.Int(required=True)
#     roles = fields.List(fields.Str(), required=True)

# class UserSetActiveSchema(Schema):
#     id = fields.Int(required=True)
#     is_active = fields.Bool(required=True)