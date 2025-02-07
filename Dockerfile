FROM python:3.9-slim

WORKDIR /app

RUN useradd -m app && chown app:app -R /app
USER app

COPY --chown=app:app . /app

ENV PATH="/home/app/.local/bin:$PATH"

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
