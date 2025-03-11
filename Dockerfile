FROM python:3.10-slim

RUN apt-get update && apt-get install -y poppler-utils

WORKDIR /app

RUN useradd -m app && chown app:app -R /app
USER app

COPY --chown=app:app . /app

ENV PATH="/home/app/.local/bin:$PATH"

RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-k", "gevent" ,"--timeout", "120", "--log-level=debug", "--bind", "0.0.0.0:5000", "app:app"]
