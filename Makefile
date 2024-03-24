.PHONY: help build format

ALL_PY := xraygpt
help:
	@LC_ALL=C $(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/(^|\n)# Files(\n|$$)/,/(^|\n)# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

build:
	-rm -rf dist out
	stubgen xraygpt
	python3 -m hatch version post
	python3 -m build

format:
	python3 -m isort --profile black $(ALL_PY)
	python3 -m black $(ALL_PY)
	# python3 -m mypy --strict $(ALL_PY)
