FROM python:3.9-slim

WORKDIR /app

# Copy the requirements list first
COPY requirements.txt .

# Install the libraries inside the container
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the script
COPY hardness.py .

CMD ["python", "hardness.py"]