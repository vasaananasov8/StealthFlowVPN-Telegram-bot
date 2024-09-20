class RepositoryException(Exception):
    ...


class RepositoryUserNotFound(RepositoryException):
    """An exception that occurs when the user is not found."""

    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(f'User with ID {self.user_id} not found.')


class RepositoryUserCreationError(RepositoryException):
    """Exception for errors when creating a user"""
    ...


class RepositorySubscriptionCreationError(RepositoryException):
    """Exception for errors when creating a subscription"""
    ...


class RepositorySubscriptionNotFound(RepositoryException):
    """An exception that occurs when a subscription is not found."""

    def __init__(self, subscription_id: int):
        self.subscription_id = subscription_id
        super().__init__(f'Subscription with ID {self.subscription_id} not found.')


class RepositoryConnectionCreationError(RepositoryException):
    """Exception for errors when creating a connection"""
    ...


class RepositoryConnectionNotFound(RepositoryException):
    """An exception that occurs when the connection is not found."""

    def __init__(self, connection_id: int):
        self.connection_id = connection_id
        super().__init__(f'Connection with ID {self.connection_id} not found.')


class RepositoryAlreadyExist(RepositoryException):
    ...
