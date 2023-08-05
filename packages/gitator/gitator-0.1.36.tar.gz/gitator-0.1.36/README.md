# gitator
This is a [python](https://www.python.org/) class with utilities createdd to interact with [Git](https://git-scm.com/) and [GitHub](https://github.com) APIs.

## Utilization
### Installation
```
pip install gitator
```

### Execution
First, import the class:
```
from gitator import Gitator
```

Then create an object and use whatever method you need:
```
gitator = Gitator()
gitator.create_github_connection(github_token)
```

## Development
### Dependencies
#### Runtime
- [PyGithub](http://pygithub.readthedocs.io/en/latest/introduction.html)

#### Tests
- [pytest](http://docs.pytest.org/en/latest/)

### Test Strategy
This script uses the [pytest](http://docs.pytest.org/en/latest/) framework in order to run unit tests.

#### Test Setup
In order to run tests, firt clone the repo and create a `virtualenv`:
```
git clone git@github.com:enkelbr/gitator.git
virtualenv -p python3 gitator
cd gitator
source bin/activate
```

Then install the deps. For example (on Enterprise Linux):
```
sudo yum install python pip
cd gitator
pip install -r requirements.txt
```

#### Test Execution
To run tests, just run pytest:
```
pytest
```
