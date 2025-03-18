init-venv:
	python -m venv venv

init:
	pip install -r requirements.txt
	
pypi:
	python setup.py sdist bdist_wheel

send:
	python -m twine upload dist/*