.PHONY: all test clean

test:
	python -m unittest -f

install:
	pip3 install -r Requirements.txt
	python3 setup.py develop

lint:
	# autopep8 -ir .
	pylint patacrep test --rcfile=pylintrc
