clean:
	find . -name __pycache__ | grep -v .virtualenv | xargs rm -rf
	find . -name "*.pyc" -exec rm -rf {} \;

tests:
	python -m unittest
