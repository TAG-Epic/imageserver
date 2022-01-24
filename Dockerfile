FROM python:3.9
COPY poetry.lock ./
COPY pyproject.toml ./
RUN poetry install
COPY . ./
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0"]
