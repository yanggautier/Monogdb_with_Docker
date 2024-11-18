FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY scripts/ /app/src/
COPY tests/ /app/tests/

CMD ["bash", "-c", "python -m pytest tests/test_connection.py && python tests/test_operation.py && python src/import_data.py && python tests/test_integrity.py && python src/export_data.py"]