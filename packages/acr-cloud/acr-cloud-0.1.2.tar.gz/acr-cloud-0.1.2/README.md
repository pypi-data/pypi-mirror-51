# ACR-Cloud
[![image](https://img.shields.io/pypi/v/acr-cloud.svg)](https://pypi.org/project/acr-cloud/)
[![image](https://img.shields.io/pypi/l/acr-cloud.svg)](https://pypi.org/project/acr-cloud/)
[![image](https://img.shields.io/pypi/pyversions/acr-cloud.svg)](https://pypi.org/project/acr-cloud/)

An ACR-Cloud API Python client library

## Installation
from PyPI
```
$ pip install acr-cloud
```

from git repository
```
$ pip install git+https://github.com/Live-Lyrics/acrcloud-py
```

from source
```
$ git clone https://github.com/Live-Lyrics/acrcloud-py
$ cd acrcloud-py
$ python setup.py install
```

## Version upgrade
```
➜ pip install --upgrade acr-cloud
```

### Requirements
* Python 3.5 and up

## Usage

Before you can begin identifying audio with ACRCloud's API, you need to sign up for a free trial over at 
https://www.acrcloud.com and create an Audio & Video recognition project. 
This will generate a `host`, `access_key`, and `access_secret` for you to use.

```python
from acr_cloud import ACRCloud

acr = ACRCloud('eu-west-1.api.acrcloud.com', 'access_key', 'access_secret')
metadata = acr.identify('path-to-file.ogg')
print(metadata)
```

## Development setup
Using [Poetry](https://poetry.eustace.io/docs/)   
```
$ poetry install
```
or [Pipenv](https://docs.pipenv.org/)   
```
$ pipenv install --dev -e .
```

## License
[MIT](https://choosealicense.com/licenses/mit/)