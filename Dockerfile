FROM cgr.dev/chainguard/python:latest-dev AS builder

WORKDIR /app

ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

COPY requirements.txt .

RUN python -m venv /app/venv && \
    python -m pip install --no-cache-dir -r requirements.txt
    

FROM cgr.dev/chainguard/python AS app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PATH="/venv/bin:$PATH"

WORKDIR /app

COPY --from=builder /app /usr/local
COPY --from=builder /app/venv /venv
COPY app.py .
COPY schema.sql .

EXPOSE 5000

ENTRYPOINT [ "python", "app.py"]