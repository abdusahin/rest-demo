# A Demo project for REST API call.

# Requirements
- Linux / MacOs
- Python 3.11
- Docker
- Make

# Setup
Create virtual environment with python3
```bash
python3 -m venv .venv
. .venv/bin/activate
```

# Building
Run command 
```bash
make build
```

# Creating Test Database
Run command 
```bash
make db
```


# Starting Application in Docker
Run command 
```bash
make up
```


# Running tests
After starting the application with make up, observe the api has started from Docker console logs, then run command 
```bash
make functional-test
```

# Viewing Records
Click on Adminer localhost port Docker Console, navigating to `http://localhost:4040/` address, login with the credentials stored in .env file

# Manual API Call
Navigate to `http://localhost:5312/docs#/` and use Swagger console to play with the API.