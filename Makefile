PYTEST := .venv/bin/pytest

.PHONY: all validate build pdf test serve

all: validate build test

validate:
	python3 scripts/build/validate_resume.py

build: validate
	python3 scripts/build/convert_resume.py

pdf:
	python3 scripts/build/generate_pdf_browser.py

test:
	$(PYTEST) tests/ -v

serve:
	python3 -m http.server 8000
