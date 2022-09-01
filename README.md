# Recruiter

## Project Description

Recruiter is system that is designed to help Recruiters and Talent Sources to find new candidates. It is a Python Bootcamp Project. The project is just a REST API service with basic functionality.

[![GitHub license](https://img.shields.io/github/license/DevIhor/Recruiter)](https://github.com/DevIhor/Recruiter/blob/main/LICENSE)
[![Pending Pull-Requests](https://img.shields.io/github/issues-pr/DevIhor/Recruiter?style=flat-square)](https://github.com/DevIhor/Recruiter/pulls)
[![GitHub top language](https://img.shields.io/github/languages/top/DevIhor/Recruiter)](https://img.shields.io/github/languages/top/DevIhor/Recruiter)

## Related Resources

- TODO

## Runtime environment

- TODO

## Commands

- TODO

## Development environment

In order to test this project on your local machine, do the following:

- Clone this repo to your local machine using the following command:

```bash
git clone https://github.com/DevIhor/Recruiter.git
```

- Navigate into the folder and install the requirements by running the following command:

```bash
cd Recruiter && pip install -r requirements.txt
```

- Make the migrations to prepare the database:

```bash
python manage.py migrate
```

- Run the server by the following command:

```bash
python manage.py runserver
```

The project should be available on your localhost, check the output of your command line for the details.

## Test environment

We are using [coverage.py](https://coverage.readthedocs.io/en/6.4.4/) for testing and coverage.
Run the tests by running:

```bash
coverage run manage.py test
```

## Deployment instructions

- TODO
