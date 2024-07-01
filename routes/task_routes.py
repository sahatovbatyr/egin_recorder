from typing import List

from flask import Blueprint, request

from models import UserRole
from services.task_service import TaskService
from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity, get_current_user

from services.user_service import UserService

task_bp = Blueprint('task_bp', __name__)


def author_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        task_id = kwargs.get('task_id')
        task = TaskService.get_task_by_id(task_id)
        if task.author_id != current_user_id:
            return {'message': 'Вы не являетесь автором этой задачи'}, 403
        return fn(*args, **kwargs)
    return wrapper

@task_bp.route('/api/task/create', methods=['POST'])
@jwt_required()
def create_task():
    """
    Создание новой задачи
    POST /api/task/create
    """
    data = request.get_json()
    return TaskService.create_task(data)

@task_bp.route('/api/task/update/<int:task_id>', methods=['PUT'])
@author_required
def update_task(task_id):
    """
    Изменение данных задачи
    PUT /api/task/update/<int:task_id>
    """
    data = request.get_json()
    return TaskService.update_task(task_id, data)

@task_bp.route('/api/task/set-done/<int:task_id>', methods=['PATCH'])
@author_required
def set_done(task_id):
    """
    Установка статуса выполнения задачи
    PATCH /api/task/set-done/<int:task_id>
    """
    return TaskService.set_task_done(task_id)

@task_bp.route('/api/task/delete/<int:task_id>', methods=['DELETE'])
@author_required
def delete_task(task_id):
    """
    Удаление задачи
    DELETE /api/task/delete/<int:task_id>
    """
    return TaskService.delete_task(task_id)
