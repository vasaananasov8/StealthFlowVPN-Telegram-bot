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


class RepositorySubscriptionCreationError(RepositoryException):
    """Исключение для ошибок при создании подписки"""
    ...


class RepositorySubscriptionNotFound(RepositoryException):
    """Исключение, которое возникает, когда подписка не найдена."""

    def __init__(self, subscription_id: int):
        self.subscription_id = subscription_id
        super().__init__(f'Subscription with ID {self.subscription_id} not found.')


class RepositoryConnectionCreationError(RepositoryException):
    """Исключение для ошибок при создании подключения"""
    ...
