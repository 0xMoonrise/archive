include .env
export

DATE := $(shell date '+%Y-%m-%d')

#Standard development environment
VENV_DIR=dev
ENV_FILE=.env
PYTHON=python3


define DOT_ENV
DB_USER=
DB_NAME=
SECRET_KEY=
DB_NAME=
endef


env: $(VENV_DIR) $(ENV_FILE)
	@echo "[+] Environment setup complete."
	. $(VENV_DIR)/bin/activate && pip install -r requirements.txt

$(VENV_DIR):
	@echo "[+] Creating virtual environment..."
	@$(PYTHON) -m venv $(VENV_DIR)
	@echo "[+] Virtual environment created in $(VENV_DIR)."

$(ENV_FILE):
	@echo "[+] Creating .env file..."
	@echo "$$DOT_ENV" > $(ENV_FILE)
	@echo "[+] .env file created. Edit it with your values."


# Docker rules


build:
	docker build -t archive	.

run:
	docker run --name archive -d -v $(CURDIR)/lectures:/app/lectures -p 5000:5000 archive

stop:
	docker stop archive || true

backup:
	docker exec -it archive_db pg_dump -U $(DB_USER) -d $(DB_NAME) --data-only | gzip > /tmp/archive_db$(DATE).gz
	# docker exec -it archive_db pg_dump -U postgresql -d archive -Fc --compress=9 -f /tmp/$(DATE).tar
	# docker cp archive_db:/tmp/$(DATE).tar ~/

restore:
	gunzip -c /tmp/archive_db$(DATE).gz | docker exec -i archive_db psql -U $(DB_USER) -h localhost -d $(DB_NAME)

clean: stop
	docker rm archive || true
	docker rmi archive:latest || true
	docker rmi python:3.10-slim || true
