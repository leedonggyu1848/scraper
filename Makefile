.PHONY: build run clean

build:
	docker-compose build

run:
	touch sent_ids.txt
	docker-compose run --rm scraper

clean:
	docker-compose down -v
