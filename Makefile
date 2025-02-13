build:
	docker build -t archive	.

run:
	docker run --name archive -d -v $(CURDIR)/lectures:/app/lectures -p 5000:5000 archive

stop:
	docker stop archive || true

clean: stop
	docker rm archive || true
	docker rmi archive:latest || true 
	docker rmi python:3.10-slim || true
