import json
import os
import dredd_hooks
import requests
import logging

response_stash = {}

print("Hooks file is executed!")


@dredd_hooks.before_each
def add_token_to_headers(transaction):
    access_token = os.getenv("ACCESS_TOKEN")

    if access_token:
        transaction["request"]["headers"]["Authorization"] = f"Bearer {access_token}"
    else:
        print("Warning: ACCESS_TOKEN environment variable is not set!")


def add_non_admin_token_to_headers(transaction):
    access_token = os.getenv("NON_ADMIN_ACCESS_TOKEN")

    if access_token:
        transaction["request"]["headers"]["Authorization"] = f"Bearer {access_token}"
    else:
        print("Warning: NON_ADMIN_ACCESS_TOKEN environment variable is not set!")


def replace_id_in_transaction(transaction, key):
    transaction["fullPath"] = transaction["origin"]["resourceName"].replace(
        f"{{{key}}}", response_stash[key]
    )
    transaction["request"]["uri"] = transaction["origin"]["resourceName"].replace(
        f"{{{key}}}", response_stash[key]
    )


@dredd_hooks.before(
    "/api/v1/expense-categories > Get Categories > 403 > application/json"
)
def fail_get_categories_403(transaction):
    add_non_admin_token_to_headers(transaction)


@dredd_hooks.before(
    "/api/v1/expense-categories > Create Category > 422 > application/json"
)
def fail_create_category_422(transaction):
    transaction["request"]["body"] = json.dumps({"description": 1, "name": 1})


@dredd_hooks.before(
    "/api/v1/expense-categories > Create Category > 403 > application/json"
)
def fail_create_category_403(transaction):
    add_non_admin_token_to_headers(transaction)


@dredd_hooks.after(
    "/api/v1/expense-categories > Create Category > 201 > application/json"
)
def stash_category_id(transaction):
    response = json.loads(transaction["real"]["body"])
    response_stash["category_id"] = response["id"]


@dredd_hooks.before(
    "/api/v1/expense-categories/{category_id} > Update Category > 200 > application/json"
)
def before_update_expense_category(transaction):
    replace_id_in_transaction(transaction, "category_id")


@dredd_hooks.before(
    "/api/v1/expense-categories/{category_id} > Update Category > 422 > application/json"
)
def fail_update_expense_category_422(transaction):
    transaction["request"]["body"] = json.dumps({"description": 1, "name": 1})


@dredd_hooks.before(
    "/api/v1/expense-categories/{category_id} > Update Category > 403 > application/json"
)
def fail_update_expense_category_403(transaction):
    replace_id_in_transaction(transaction, "category_id")
    add_non_admin_token_to_headers(transaction)


@dredd_hooks.before("/api/v1/expenses > Create Expense > 201 > application/json")
def create_expense(transaction):
    requestBody = json.loads(transaction["request"]["body"])
    requestBody["category_id"] = response_stash["category_id"]
    transaction["request"]["body"] = json.dumps(requestBody)


@dredd_hooks.after("/api/v1/expenses > Create Expense > 201 > application/json")
def stash_expense_id(transaction):
    response = json.loads(transaction["real"]["body"])
    response_stash["expense_id"] = response["id"]


@dredd_hooks.before("/api/v1/expenses > Create Expense > 422 > application/json")
def fail_create_expense_422(transaction):
    requestBody = json.loads(transaction["request"]["body"])
    transaction["request"]["body"] = json.dumps(
        {
            **requestBody,
            "name": 1,
            "description": 1,
            "category_id": response_stash["category_id"],
        }
    )


@dredd_hooks.before(
    "/api/v1/expenses/{expense_id} > Get Expense > 200 > application/json"
)
def before_get_expense(transaction):
    replace_id_in_transaction(transaction, "expense_id")


@dredd_hooks.before(
    "/api/v1/expenses/{expense_id} > Update Expense > 200 > application/json"
)
def before_put_expense(transaction):
    replace_id_in_transaction(transaction, "expense_id")
    requestBody = json.loads(transaction["request"]["body"])
    requestBody["category_id"] = response_stash["category_id"]
    transaction["request"]["body"] = json.dumps(requestBody)


@dredd_hooks.before(
    "/api/v1/expenses/{expense_id} > Update Expense > 422 > application/json"
)
def fail_put_expense_422(transaction):
    replace_id_in_transaction(transaction, "expense_id")
    transaction["request"]["body"] = json.dumps(
        {
            "name": 1,
            "description": 1,
            "amount": "test",
        }
    )


@dredd_hooks.before("/api/v1/expenses/{expense_id} > Delete Expense > 204")
def before_delete_expense(transaction):
    replace_id_in_transaction(transaction, "expense_id")
