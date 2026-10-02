FROM python:3.14.7-slim

WORKDIR /app

RUN apt-get update && \
    apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*


COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip "setuptools>=78.1.1" && \
    pip install --no-cache-dir --root-user-action=ignore -r requirements.txt && \
    pip uninstall -y setuptools

COPY . .

CMD ["python", "src/41_scan_stream_default.py"]
