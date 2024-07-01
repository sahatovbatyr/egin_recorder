from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from extensions import ma
from models import Task

class TaskCreateDto(Schema):
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    author_id = fields.Int(required=True)
    assigned_to_id = fields.Int(required=True)

class TaskCreateSchema(Schema):
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    author_id = fields.Int(required=True)
    assigned_to_id = fields.Int()

class TaskUpdateSchema(Schema):
    id = fields.Int(required=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    assigned_to_id = fields.Int()

class TaskSetDoneSchema(Schema):
    id = fields.Int(required=True)
    is_done = fields.Bool(required=True)

class TaskDeleteSchema(Schema):
    id = fields.Int(required=True)