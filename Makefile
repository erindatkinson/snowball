all: build

## build:		builds the bot container
build: 
	docker-compose build

## run:		builds and starts the bot container
run: build
	docker-compose up -d

## migrate:		migrate db schema
migrate:
	migrate -source file://migrations -database sqlite3://data/snowball.db up

## help:		prints make target help information from comments in makefile.
help: Makefile
	@sed -n 's/^##//p' $< | sort

.PHONY: help run build all