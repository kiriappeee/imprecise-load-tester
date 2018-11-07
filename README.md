# Basic and imprecise load testing

## Usage instructions

* Make sure you've installed `python3` and `pipenv`
* Clone the repo
* Run `pipenv install --three`
* Copy `tests.example.yaml` to `tests.yaml`
* Edit `tests.yaml` as needed (explaining of values given below)
* Run `pipenv run python load.py`
* Check the generated `-results.txt` files for your results

## `tests.yaml` options

`tests` is the top level array that must be present in the file. Each item has the following
elements:

* `name`: Used to generate the results files (`name-results.txt`). Program does not check for uniqueness.
* `url`: Url to load test
* `iterations`: Number of times to load the url
* `enabled` (OPTIONAL): Defaults to `true`. Use `false` if you want to disable a test.
* `verify` (OPTIONAL): Defaults to `true`. Use `false` if you want to test against a URL without a matching SSL cert.