from marshmallow import Schema, fields


class AuthRequestDto(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)