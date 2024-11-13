
FROM python:3.9

WORKDIR /app


COPY requirements.txt requirements.txt

# Install system dependencies and Python dependencies
# Install gcc and other build tools for compiling packages like netifaces
RUN pip install --no-cache-dir --upgrade -r requirements.txt


COPY ./src /app


CMD ["uvicorn", "__init__:app", "--host", "0.0.0.0", "--port", "8000"]
