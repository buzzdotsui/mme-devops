FROM python:3.9-slim

WORKDIR /app

# Copy the requirements list first
COPY requirements.txt .

# Install the libraries inside the container
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY main.py .
COPY hardness.py .
COPY mme_calc/ ./mme_calc/

CMD ["python", "main.py"]