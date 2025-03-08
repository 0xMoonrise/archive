build:
	docker build -t archive	.

run:
	docker run --name archive -d -v $(CURDIR)/lectures:/app/lectures -p 5000:5000 archive

stop:
	docker stop archive || true

backup:
	docker exec -it archive_db pg_dump -U postgresql -d archive -Fc -f /tmp/$(date +'%Y-%m-%d').tar
	docker cp archive_db:/tmp/$(date +'%Y-%m-%d').tar /opt/backups

restore:
	

clean: stop
	docker rm archive || true
	docker rmi archive:latest || true
	docker rmi python:3.10-slim || true
