.PHONY: start lint format typecheck test clean

start:
	uv run python run.py

test:
	uv run pytest -v tests/ --cov=gameoflife/

lint:
	uv run ruff check .

format:
	uv run ruff format .

typecheck:
	uv run ty check

clean:
	rm -rf .coverage
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type d -name '.*_cache' -exec rm -rf {} +
	uv cache clear