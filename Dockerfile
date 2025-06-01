FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml ./
RUN pip install --no-cache-dir poetry && poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi
COPY ipfs_onboarder ./ipfs_onboarder
CMD ["uvicorn", "ipfs_onboarder.main:app", "--host", "0.0.0.0", "--port", "8000"]
