class UserNotFoundException(Exception):
    def __init__(self, user_id:int):
        self.message = f'User with id {user_id} not found'
        self.status_code = 404
        super().__init__(self.message)

class UserExistsException(Exception):
    def __init__(self, username:str):
        self.message = f'User with {username} already exists.'
        self.status_code = 400
        super().__init__(self.message)

class AccessDeniedException(Exception):
    def __init__(self, message:str):
        self.message = f'Access denied. {message}'
        self.status_code = 400
        super().__init__(self.message)


class ResourceNotFoundException(Exception):
    def __init__(self, resource_type, resource_id):
        self.message = f'{resource_type} with id {resource_id} not found'
        super().__init__(self.message)
