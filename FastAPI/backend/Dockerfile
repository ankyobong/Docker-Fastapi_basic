FROM python:3.8.6

# ==============================================================================
# 타임존 설정
ENV PYTHONUNBUFFERED=0

RUN #apk add --no-cache --virtual .build-deps gcc musl-dev

# ==============================================================================
#RUN mkdir -p /backend
#ADD backend /backend

# ==============================================================================
# 파일 복사
COPY . FastAPI/backend
WORKDIR FastAPI/backend

# ==============================================================================
# 설치
RUN python -m pip install pip --upgrade
RUN pip install -r requirements.txt

CMD uvicorn --host=0.0.0.0 --port 8000 backend:app
