# Colors
Color_Off=\033[0m
Cyan=\033[1;36m

help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

build:  ## Сборка проекта
	@echo -e '${Cyan}Сборка проекта${Color_Off}'
	@docker-compose build

start:  ## Запустить проект
	@docker-compose up -d forum_api

stop:  ## Остановить проект
	@docker-compose down

test:  ## Запустить тесты
	@@docker-compose run test

.PHONY: help, build, start, stop, test
.DEFAULT_GOAL := help
