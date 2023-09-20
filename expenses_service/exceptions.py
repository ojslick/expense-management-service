class ExpenseNotFoundError(Exception):
    def __init__(self, message):
        self.message = message


class APIIntegrationError(Exception):
    pass


class InvalidActionError(Exception):
    pass
