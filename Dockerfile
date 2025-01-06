FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml /app/
COPY requirements.txt /app/
COPY game /app/game/

RUN pip install --upgrade pip \
    && pip install build \
    && python -m build --wheel --outdir dist \
    && pip install dist/*.whl

EXPOSE 5555

CMD ["python","-u", "game/server/multiplayer_server.py"]
