DATE := $(shell date '+%Y-%m-%d')

build:
	docker build -t archive	.

run:
	docker run --name archive -d -v $(CURDIR)/lectures:/app/lectures -p 5000:5000 archive

stop:
	docker stop archive || true

backup:
	docker exec -it archive_db pg_dump -U postgresql -d archive -Fc --compress=9 -f /tmp/$(DATE).tar
	docker cp archive_db:/tmp/$(DATE).tar ~/

clean: stop
	docker rm archive || true
	docker rmi archive:latest || true
	docker rmi python:3.10-slim || true
