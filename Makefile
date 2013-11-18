clean:
	find . -name __pycache__ | grep -v .virtualenv | xargs rm -rf

tests:
	python -m unittest
