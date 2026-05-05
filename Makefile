PYTEST := /Users/tom/Library/Python/3.9/bin/pytest

.PHONY: all validate build pdf test serve

all: validate build test

validate:
	python3 scripts/validate_resume.py

build: validate
	python3 scripts/convert_resume.py

pdf:
	python3 scripts/generate_pdf_browser.py

test:
	$(PYTEST) tests/ -v

serve:
	python3 -m http.server 8000
