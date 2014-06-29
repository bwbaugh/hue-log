.PHONY: clean

venv: venv/bin/activate

venv/bin/activate: requirements.txt
	test -d venv || virtualenv --no-site-packages --python /usr/bin/python venv
	. venv/bin/activate; pip install --upgrade -r requirements.txt
	touch venv/bin/activate

clean:
	find . -name '*.pyc' -delete
	rm -rf docs/build/*
	rm -rf .tox/
	rm -rf venv/
