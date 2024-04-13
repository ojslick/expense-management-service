FROM python:3.9-slim

RUN apt-get update && apt-get install -y libpq-dev

WORKDIR /expense_management

RUN pip install -U pip && pip install pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system --deploy

COPY expenses_service /expense_management/expenses_service
COPY repository /expense_management/repository
COPY schemas /expense_management/schemas
COPY web /expense_management/web
COPY oas.yaml /expense_management/oas.yaml
COPY public_key.pem /expense_management/public_key.pem
COPY private_key.pem /expense_management/private_key.pem

EXPOSE 8000

CMD ["uvicorn", "web.app:app", "--host", "0.0.0.0"]