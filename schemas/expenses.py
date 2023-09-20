from datetime import datetime

from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, condate, Extra


class ExpenseCategorySchema(BaseModel):
    name: str
    description: Optional[str] = None

    class Config:
        extra = Extra.forbid
        json_schema_extra = {
            "example": {"name": "Food", "description": "Food expenses"}
        }


class CreateExpenseCategorySchema(BaseModel):
    name: str
    description: str

    class Config:
        extra = Extra.forbid
        json_schema_extra = {
            "example": {"name": "Food", "description": "Food expenses"}
        }


class GetExpenseCategorySchema(CreateExpenseCategorySchema):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        extra = Extra.forbid
        json_schema_extra = {
            "example": {
                "id": "d290f1ee-6c54-4b01-90e6-d701748f0851",
                "name": "Food",
                "description": "Food expenses",
                "created_at": "2021-01-01T00:00:00.000Z",
                "updated_at": "2021-01-01T00:00:00.000Z",
            }
        }


class GetExpenseCategoriesSchema(BaseModel):
    categories: List[GetExpenseCategorySchema]

    class Config:
        extra = Extra.forbid
        json_schema_extra = {
            "example": {
                "categories": [
                    {
                        "id": "d290f1ee-6c54-4b01-90e6-d701748f0851",
                        "name": "Food",
                        "description": "Food expenses",
                        "created_at": "2021-01-01T00:00:00.000Z",
                        "updated_at": "2021-01-01T00:00:00.000Z",
                    }
                ]
            }
        }


class ExpenseSchema(BaseModel):
    id: UUID
    user_id: str
    amount: float
    category_id: UUID
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    category: GetExpenseCategorySchema

    class Config:
        extra = Extra.forbid
        json_schema_extra = {
            "example": {
                "id": "d290f1ee-6c54-4b01-90e6-d701748f0851",
                "user_id": "d290f1ee-6c54-4b01-90e6-d701748f0851",
                "amount": 100.0,
                "category_id": "d290f1ee-6c54-4b01-90e6-d701748f085",
                "name": "Food expenses",
                "description": "Food expenses description",
                "created_at": "2021-01-01T00:00:00.000Z",
                "updated_at": "2021-01-01T00:00:00.000Z",
                "category": {
                    "id": "d290f1ee-6c54-4b01-90e6-d701748f0851",
                    "name": "Food",
                    "description": "Food expenses",
                    "created_at": "2021-01-01T00:00:00.000Z",
                    "updated_at": "2021-01-01T00:00:00.000Z",
                },
            }
        }


class CreateExpenseSchema(BaseModel):
    amount: float
    category_id: str
    name: str
    description: str

    class Config:
        extra = Extra.forbid
        json_schema_extra = {
            "example": {
                "amount": 100.0,
                "category_id": "d290f1ee-6c54-4b01-90e6-d701748f085",
                "name": "Food expenses",
                "description": "Food expenses description",
            }
        }


class GetExpenseSchema(CreateExpenseSchema):
    id: UUID
    user_id: str
    created_at: datetime
    updated_at: datetime
    category: GetExpenseCategorySchema

    class Config:
        extra = Extra.forbid
        json_schema_extra = {
            "example": {
                "id": "d290f1ee-6c54-4b01-90e6-d701748f0851",
                "user_id": "d290f1ee-6c54-4b01-90e6-d701748f0851",
                "amount": 100.0,
                "category_id": "d290f1ee-6c54-4b01-90e6-d701748f085",
                "description": "Food expenses",
                "created_at": "2021-01-01T00:00:00.000Z",
                "updated_at": "2021-01-01T00:00:00.000Z",
                "category": {
                    "id": "d290f1ee-6c54-4b01-90e6-d701748f0851",
                    "name": "Food",
                    "description": "Food expenses",
                    "created_at": "2021-01-01T00:00:00.000Z",
                    "updated_at": "2021-01-01T00:00:00.000Z",
                },
            }
        }


class GetExpensesSchema(BaseModel):
    expenses: List[GetExpenseSchema]

    class Config:
        extra = Extra.forbid
        json_schema_extra = {
            "example": {
                "expenses": [
                    {
                        "id": "d290f1ee-6c54-4b01-90e6-d701748f0851",
                        "amount": 100.0,
                        "category_id": "d290f1ee-6c54-4b01-90e6-d701748f085",
                        "name": "Food expenses",
                        "description": "Food expenses description",
                        "created_at": "2021-01-01T00:00:00.000Z",
                        "updated_at": "2021-01-01T00:00:00.000Z",
                        "category": {
                            "id": "d290f1ee-6c54-4b01-90e6-d701748f0851",
                            "name": "Food",
                            "description": "Food expenses",
                            "created_at": "2021-01-01T00:00:00.000Z",
                            "updated_at": "2021-01-01T00:00:00.000Z",
                        },
                    }
                ]
            }
        }
