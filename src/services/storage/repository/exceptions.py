class RepositoryException(Exception):
    ...


class RepositoryUserNotFound(RepositoryException):
    """Исключение, которое возникает, когда пользователь не найден."""
    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(f'User with ID {self.user_id} not found.')


class RepositoryUserCreationError(RepositoryException):
    """Исключение для ошибок при создании пользователя"""
    ...
