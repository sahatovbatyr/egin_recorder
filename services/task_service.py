from models import db, Task, User
from schemas.task_schemas import TaskCreateDto
from sqlalchemy.exc import IntegrityError

class TaskService:

    @staticmethod
    def create_task(taskCreateDto: TaskCreateDto):
        new_task = Task(title=taskCreateDto.title, description=taskCreateDto.description)
        new_task.author_id = taskCreateDto.author_id
        if taskCreateDto.assigned_to_id:
            new_task.assigned_to_id = taskCreateDto.assigned_to_id

        try:
            db.session.add(new_task)
            db.session.commit()
            return {'message': 'Задача успешно создана'}, 201
        except IntegrityError:
            db.session.rollback()
            return {'message': 'Ошибка создания задачи'}, 400

    # @staticmethod
    # def update_task(task_id, task_data: TaskUpdateDTO):
    #     task = Task.query.get(task_id)
    #     task.title = task_data.title
    #     task.description = task_data.description
    #
    #     try:
    #         db.session.commit()
    #         return {'message': 'Данные задачи успешно изменены'}, 200
    #     except IntegrityError:
    #         db.session.rollback()
    #         return {'message': 'Ошибка изменения данных задачи'}, 400

    @staticmethod
    def set_task_done(task_id):
        task = Task.query.get(task_id)
        task.is_done = True

        try:
            db.session.commit()
            return {'message': 'Статус выполнения задачи успешно изменен'}, 200
        except IntegrityError:
            db.session.rollback()
            return {'message': 'Ошибка изменения статуса выполнения задачи'}, 400

    @staticmethod
    def delete_task(task_id):
        task = Task.query.get(task_id)

        try:
            db.session.delete(task)
            db.session.commit()
            return {'message': 'Задача успешно удалена'}, 200
        except IntegrityError:
            db.session.rollback()
            return {'message': 'Ошибка удаления задачи'}, 400
