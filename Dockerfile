FROM python:3.10.11

WORKDIR /workspace

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

COPY src src
COPY tests tests
COPY alembic.ini .

COPY .flake8 .
COPY .ruff.toml .
COPY mypy.ini .
COPY pytest.ini .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
