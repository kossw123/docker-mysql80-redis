# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# ✅ requirements 먼저 복사
COPY requirements.txt .

# ✅ 의존성 설치 (이게 핵심)
RUN pip install --no-cache-dir -r requirements.txt

# ✅ 전체 코드 복사
COPY . .

# ✅ 권한 문제 방지 (선택)
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

# ⚠️ 경로는 프로젝트 구조에 따라 맞춰야 함
CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=8000"]