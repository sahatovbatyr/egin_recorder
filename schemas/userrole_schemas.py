from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

from models import UserRole


class UserRoleSchema(SQLAlchemySchema):
    class Meta:
        model = UserRole
        load_instance = True

    id = auto_field()
    title = auto_field()