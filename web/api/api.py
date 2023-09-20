import casbin
from datetime import datetime
from uuid import UUID
from fastapi import APIRouter as Router, HTTPException, Depends

from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN,
)

from schemas.expenses import (
    CreateExpenseSchema,
    ExpenseSchema,
    GetExpensesSchema,
    GetExpenseSchema,
    GetExpenseCategorySchema,
    CreateExpenseCategorySchema,
    GetExpenseCategorySchema,
    GetExpenseCategoriesSchema,
)
from typing import Optional

from repository.expenses_repository import ExpensesRepository
from repository.unit_of_work import UnitOfWork
from expenses_service.expenses_service import ExpensesService
from expenses_service.exceptions import ExpenseNotFoundError

from web.app import app

app = Router()


@app.get("/expenses", response_model=GetExpensesSchema)
def get_expenses(request: Request, limit: Optional[int] = None):
    with UnitOfWork() as unit_of_work:
        repository = ExpensesRepository(unit_of_work.session)
        service = ExpensesService(repository)
        expenses = service.list_expenses(
            limit=limit, user_id=request.state.user_details["user_id"]
        )
        return {"expenses": expenses}


@app.get("/expenses/{expense_id}", response_model=ExpenseSchema)
def get_expense(request: Request, expense_id: UUID):
    with UnitOfWork() as unit_of_work:
        repository = ExpensesRepository(unit_of_work.session)
        service = ExpensesService(repository)
        expense = service.get_expense(
            expense_id, user_id=request.state.user_details["user_id"]
        )
        if expense is None:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail=f"Expense with id {expense_id} not found",
            )
        return expense


@app.post("/expenses", response_model=GetExpenseSchema, status_code=HTTP_201_CREATED)
def create_expense(request: Request, payload: CreateExpenseSchema):
    with UnitOfWork() as unit_of_work:
        repository = ExpensesRepository(unit_of_work.session)
        service = ExpensesService(repository)
        expense = service.add_expense(
            request.state.user_details["user_id"], expense=payload.dict()
        )
        unit_of_work.commit()
        return expense.dict()


@app.put("/expenses/{expense_id}", response_model=GetExpenseSchema)
def update_expense(request: Request, expense_id: UUID, payload: CreateExpenseSchema):
    try:
        with UnitOfWork() as unit_of_work:
            repository = ExpensesRepository(unit_of_work.session)
            service = ExpensesService(repository)
            expense = service.update_expense(
                expense_id,
                user_id=request.state.user_details["user_id"],
                _expense=payload.dict(),
            )
            unit_of_work.commit()
            return expense
    except ExpenseNotFoundError as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=e.message)


@app.delete(
    "/expenses/{expense_id}",
    status_code=HTTP_204_NO_CONTENT,
    response_class=JSONResponse,
)
def delete_expense(request: Request, expense_id: UUID):
    try:
        with UnitOfWork() as unit_of_work:
            repository = ExpensesRepository(unit_of_work.session)
            service = ExpensesService(repository)
            service.delete_expense(
                expense_id, user_id=request.state.user_details["user_id"]
            )
            unit_of_work.commit()
        return
    except ExpenseNotFoundError as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=e.message)


@app.get(
    "/expense-categories",
    response_model=GetExpenseCategoriesSchema,
)
def get_categories(request: Request):
    if request.state.user_details["user_role"] == "admin":
        with UnitOfWork() as unit_of_work:
            repository = ExpensesRepository(unit_of_work.session)
            service = ExpensesService(repository)
            categories = service.list_categories()
            return {"categories": categories}
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Only admin users can access this endpoint",
        )


@app.post(
    "/expense-categories",
    response_model=GetExpenseCategorySchema,
    status_code=HTTP_201_CREATED,
)
def create_category(request: Request, payload: CreateExpenseCategorySchema):
    if request.state.user_details["user_role"] == "admin":
        with UnitOfWork() as unit_of_work:
            repository = ExpensesRepository(unit_of_work.session)
            service = ExpensesService(repository)
            category = service.add_category(expenseCategory=payload.dict())
            unit_of_work.commit()
            unit_of_work.refresh(category)
            return category.dict()
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Only admin users can access this endpoint",
        )


@app.put("/expense-categories/{category_id}", response_model=GetExpenseCategorySchema)
def update_category(
    request: Request, category_id: UUID, payload: CreateExpenseCategorySchema
):
    try:
        if request.state.user_details["user_role"] == "admin":
            with UnitOfWork() as unit_of_work:
                repository = ExpensesRepository(unit_of_work.session)
                service = ExpensesService(repository)
                category = service.update_category(
                    category_id, expenseCategory=payload.dict()
                )
                unit_of_work.commit()
                return category
        else:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="Only admin users can access this endpoint",
            )
    except ExpenseNotFoundError as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=e.message)


@app.delete(
    "/expense-categories/{category_id}",
    status_code=HTTP_204_NO_CONTENT,
    response_class=JSONResponse,
)
def delete_category(request: Request, category_id: UUID):
    try:
        if request.state.user_details["user_role"] == "admin":
            with UnitOfWork() as unit_of_work:
                repository = ExpensesRepository(unit_of_work.session)
                service = ExpensesService(repository)
                service.delete_category(category_id)
                unit_of_work.commit()
                return
        else:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="Only admin users can access this endpoint",
            )
    except ExpenseNotFoundError as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=e.message)
