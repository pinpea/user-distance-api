# Flask API demo to find users near London

## Requirements

This project depends on Python 3, pip3 and virtualenv

pip3 install virtualenv

which python3
virtualenv -p /output/from/which/python3 venv

source venv/bin/activate

## Using Docker with this demo

```bash
docker build -t flask_demo .
```

running the container

```bash
docker run -d --name container_name_1 -p 5000:5000 flask_demo
```

`--name` should be unique to each instance of run, and can be used to exec commands and kill container later.

Open Web browser at localhost:5000

### Executing the tests in Docker

```bash
docker exec container_name_1 python -m pytest -s tests
```
