## Test Package

```bash
pipenv install pip setuptools whell tqdm twine
chmod +x kokoko
pipenv run python setup.py sdist bdist_wheel
pipenv run python -m twine upload dist/*
```

## Check

```bash
pipenv run pip install kokoko
pipenv run pip kokoko
```