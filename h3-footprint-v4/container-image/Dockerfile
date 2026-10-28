FROM python:3.12.10-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /opt/runner
COPY sandbox_worker.py /opt/runner/sandbox_worker.py
USER 65534:65534
ENTRYPOINT ["python", "-I", "/opt/runner/sandbox_worker.py"]
