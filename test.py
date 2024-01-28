from pathlib import Path
from fastapi.testclient import TestClient
from web.app import app
import os
import hypothesis.strategies as st
import jsonschema
import yaml
from hypothesis import given, Verbosity, settings
from jsonschema import ValidationError, RefResolver

test_client = TestClient(app=app)
admin_access_token = os.getenv("ACCESS_TOKEN")
non_admin_access_token = os.getenv("NON_ADMIN_ACCESS_TOKEN")

expense_management_api_spec = yaml.full_load(
    (Path(__file__).parent / "oas.yaml").read_text()
)

create_expense_schema = expense_management_api_spec["components"]["schemas"][
    "CreateExpenseSchema"
]

values_strategy = st.none() | st.booleans() | st.text() | st.text() | st.integers()

expense_item_strategy = st.fixed_dictionaries(
    {
        "amount": values_strategy,
        "category_id": values_strategy,
        "name": values_strategy,
        "description": values_strategy,
    }
)

strategy = st.fixed_dictionaries({"expense": st.lists(expense_item_strategy)})


def is_valid_payload(payload, schema):
    try:
        jsonschema.validate(
            payload, schema, resolver=RefResolver("", expense_management_api_spec)
        )
    except ValidationError:
        return False
    return True


@given(strategy)
def test_create_expense(payload):
    response = test_client.post(
        "/api/v1/expense-categories",
        json=payload,
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    if is_valid_payload(payload, create_expense_schema):
        assert response.status_code == 201
    else:
        assert response.status_code == 422


def test_get_expenses():
    response = test_client.get(
        "/api/v1/expenses",
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    assert response.status_code == 200
