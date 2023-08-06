# Example Z Package

This is a simple z package. 


518  python3 setup.py sdist bdist_wheel
519  python -m twine upload dist/*
520  pip install zsearch

516  vi ~/.pypirc

[distutils]
index-servers=pypi
[pypi]
repository = https://upload.pypi.org/legacy/
username =azeltov