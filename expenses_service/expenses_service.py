from expenses_service.exceptions import ExpenseNotFoundError


class ExpensesService:
    def __init__(self, expenses_repository):
        self.expenses_repository = expenses_repository

    def add_expense(self, user_id, expense):
        return self.expenses_repository.add(expense, user_id)

    def get_expense(
        self,
        expense_id,
    ):
        expense = self.expenses_repository.get(
            expense_id,
        )
        return expense

    def list_expenses(self, **filters):
        return self.expenses_repository.list(**filters)

    def update_expense(self, expense_id, _expense, **filters):
        expense = self.expenses_repository.get(expense_id, **filters)
        if expense is None:
            raise ExpenseNotFoundError(f"Expense with id {expense_id} not found")
        return self.expenses_repository.update(expense_id, _expense)

    def delete_expense(self, expense_id, **filters):
        expense = self.expenses_repository.get(expense_id, **filters)
        if expense is None:
            raise ExpenseNotFoundError(f"Expense with id {expense_id} not found")
        return self.expenses_repository.delete(expense_id)

    def add_category(self, expenseCategory):
        return self.expenses_repository.add_category(expenseCategory)

    def list_categories(self):
        return self.expenses_repository.list_categories()

    def update_category(self, category_id, expenseCategory):
        category = self.expenses_repository.get_category(category_id)
        if category is None:
            raise ExpenseNotFoundError(
                f"Expense category with id {category_id} not found"
            )
        return self.expenses_repository.update_category(category_id, expenseCategory)

    def delete_category(self, category_id):
        category = self.expenses_repository.get_category(category_id)
        if category is None:
            raise ExpenseNotFoundError(
                f"Expense category with id {category_id} not found"
            )
        return self.expenses_repository.delete_category(category_id)
