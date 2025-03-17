include .env
export
DATE := $(shell date '+%Y-%m-%d')

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
