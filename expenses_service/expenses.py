import requests
from expenses_service.exceptions import APIIntegrationError, InvalidActionError

class Expenses:
    def __init__(
        self,
        id=None,
        amount=None,
        category_id=None,
        description=None,
        created_at=None,
        updated_at=None,
        category=None
    ):
        self.id = id
        self.amount = amount
        self.category_id = category_id
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at
        self.category = category
        
    