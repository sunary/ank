.PHONY: help install test run build clean sdist create

PYTHON ?= python

help:
	@echo "ANK - Python streaming system"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  help      Show this help (default)"
	@echo "  install   Install ank in editable mode (pip install -e .)"
	@echo "  test      Run unit tests"
	@echo "  run       Run service (from examples/streaming_app)"
	@echo "  build     Build Docker image"
	@echo "  clean     Remove build artifacts and caches"
	@echo "  sdist     Build source distribution"
	@echo "  create    Create example project (TestService)"

install:
	pip install -e .

test:
	$(PYTHON) -m unittest discover -s ank/tests -p 'test_*.py' -v

run:
	cd examples/streaming_app && ank run -fs settings.yml

build:
	docker build -t ank .

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete 2>/dev/null || true

sdist: clean
	$(PYTHON) setup.py sdist

create:
	ank create TestService -c BaseApp
