import schemathesis
import os

schema = schemathesis.from_uri(
    "http://localhost:8000/api/v1/expenses/openapi.json",
    headers={"Authorization": f'Bearer {os.getenv("ACCESS_TOKEN")}'},
)

schema.add_link(
    source=schema["/api/v1/expense-categories"]["POST"],
    target=schema["/api/v1/expenses/{expense_id}"]["GET"],
    status_code=201,
    parameters={"expense_id": "$response.body#/id"},
    request_body={
        "expense": {
            "amount": 10.0,
            "category_id": "$response.body#/id",
            "name": "test",
            "description": "test",
        }
    },
)


@schema.parametrize()
def test_api_behaviour(case):
    case.call_and_validate(
        headers={"Authorization": f'Bearer {os.getenv("ACCESS_TOKEN")}'}
    )
