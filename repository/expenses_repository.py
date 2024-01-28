from repository.models import ExpenseModel, ExpenseCategoryModel
from datetime import datetime


class ExpensesRepository:
    def __init__(self, session):
        self.session = session

    def add(self, expense, user_id):
        record = ExpenseModel(**expense, user_id=user_id)
        self.session.add(record)
        return record

    def _get(self, id, model, **filters):
        return self.session.query(model).filter(model.id == str(id)).first()

    def get(self, expense_id):
        record = self._get(id=expense_id, model=ExpenseModel)
        if record is not None:
            return record.dict()

    def list(self, **filters):
        query = self.session.query(ExpenseModel)
        if filters:
            query = query.filter_by(**filters)
        return [record.dict() for record in query.all()]

    def update(self, expense_id, expense, **filters):
        record = self._get(expense_id, ExpenseModel, **filters)
        if record is not None:
            for key, value in expense.items():
                setattr(record, key, value)
            record.updated_at = datetime.utcnow()
            self.session.add(record)
            return record.dict()

    def delete(self, expense_id):
        record = self._get(expense_id, ExpenseModel)
        if record is not None:
            self.session.delete(record)

    def add_category(self, expenseCategory):
        record = ExpenseCategoryModel(**expenseCategory)
        self.session.add(record)
        return record

    def get_category(self, category_id):
        record = self._get(category_id, ExpenseCategoryModel)
        if record is not None:
            return record.dict()

    def list_categories(self):
        query = self.session.query(ExpenseCategoryModel)
        return [record.dict() for record in query.all()]

    def update_category(self, category_id, expenseCategory):
        record = self._get(category_id, ExpenseCategoryModel)
        if record is not None:
            for key, value in expenseCategory.items():
                setattr(record, key, value)
            record.updated_at = datetime.utcnow()
            self.session.add(record)
            return record.dict()

    def delete_category(self, category_id):
        record = self._get(category_id, ExpenseCategoryModel)
        if record is not None:
            self.session.delete(record)
