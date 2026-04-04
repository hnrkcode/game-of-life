.PHONY:
	start
	pygbag
	build
	lint
	format
	typecheck
	test
	clean

start:
	uv run python main.py

pygbag:
	uv run pygbag \
		--title "GAME OF LIFE" \
		--width 1280 \
		--height 720 \
		--icon data/images/logo.png \
		.

build:
	uv run pygbag \
		--build \
		--archive \
		--title "GAME OF LIFE" \
		--package hnrkcode-game-of-life \
		--width 1280 \
		--height 720 \
		--icon data/images/logo.png \
		.

test:
	uv run pytest -v tests/ --cov=gameoflife/

lint:
	uv run ruff check . --fix --show-fixes

format:
	uv run ruff format .

typecheck:
	uv run ty check

clean:
	rm -rf .coverage build
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type d -name '.*_cache' -exec rm -rf {} +
	uv cache clear