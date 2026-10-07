# Rebuild everything in homer/:   make -C homer   (or: make -C homer all)
# Uses the project virtualenv; override with  make -C homer PY=python3
PY ?= $(abspath $(CURDIR)/../.venv/bin/python)

.PHONY: all fetch lines tables ngrams validate clean-derived

all: lines tables ngrams validate

../corpus/raw/perseus/tlg0012.tlg001.perseus-grc2.xml ../corpus/raw/perseus/tlg0012.tlg002.perseus-grc2.xml:
	cd .. && $(PY) homer/fetch_text.py

fetch:
	cd .. && $(PY) homer/fetch_text.py

lines: ../corpus/raw/perseus/tlg0012.tlg001.perseus-grc2.xml ../corpus/raw/perseus/tlg0012.tlg002.perseus-grc2.xml
	cd .. && $(PY) homer/build_lines.py

tables: lines
	cd .. && $(PY) homer/build_tables.py

ngrams: tables
	cd .. && $(PY) homer/concordance.py --build-ngrams

validate: tables
	cd .. && $(PY) homer/validate.py
