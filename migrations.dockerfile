FROM python:3.9-slim

RUN mkdir -p /expense_management

WORKDIR /expense_management

RUN pip install -U pip && pip install pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system --deploy

COPY repository /expense_management/repository
COPY migrations /expense_management/migrations
COPY alembic.ini /expense_management/alembic.ini

ENV PYTHONPATH=/expense_management
CMD [ "alembic", "upgrade", "heads" ]