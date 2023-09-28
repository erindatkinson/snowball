all: build

## build:		builds the bot container
build: 
	docker-compose build

## run:		builds and starts the bot container
run: build
	docker-compose up -d

## help:		prints make target help information from comments in makefile.
help: Makefile
	@sed -n 's/^##//p' $< | sort

.PHONY: help run build all