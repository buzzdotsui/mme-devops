# 1. Use a lightweight version of Linux with Python pre-installed
FROM python:3.9-slim

# 2. Set the "folder" inside the container where our code lives
WORKDIR /app

# 3. Copy your hardness.py from your laptop into the container
COPY hardness.py .

# 4. Tell the container what command to run when it starts
CMD ["python", "hardness.py"]