# Recruiter

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#project-description">Project Description</a></li>
    <li><a href="#related-resources">Related Resources</a></li>
    <li><a href="#runtime-environment">Runtime Environment</a></li>
    <li><a href="#commands">Commands</a></li>
    <li><a href="#development-environment">Development Environment</a></li>
    <li><a href="#test-environment">Test Environment</a></li>
    <li><a href="#deployment-instructions">Deployment instructions</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## Project Description

Recruiter is system that is designed to help Recruiters and Talent Sources to find new candidates. It is a Python Bootcamp Project. The project is just a REST API service with basic functionality.

[![GitHub license](https://img.shields.io/github/license/DevIhor/Recruiter)](https://github.com/DevIhor/Recruiter/blob/main/LICENSE)
[![Pending Pull-Requests](https://img.shields.io/github/issues-pr/DevIhor/Recruiter?style=flat-square)](https://github.com/DevIhor/Recruiter/pulls)
[![GitHub top language](https://img.shields.io/github/languages/top/DevIhor/Recruiter)](https://img.shields.io/github/languages/top/DevIhor/Recruiter)

## Related Resources

The following list contains information of what is used in this project.

[![Django](https://img.shields.io/badge/Django-4.1-green?style=for-the-badge)](https://docs.djangoproject.com/en/4.1/)
[![DRF](https://img.shields.io/badge/DRF-3.13.1-green?style=for-the-badge)](https://www.django-rest-framework.org/)
[![Celery](https://img.shields.io/badge/Celery-5.2.7-green?style=for-the-badge)](https://docs.celeryq.dev/en/stable/)
[![Redis](https://img.shields.io/badge/Redis-4.3.4-green?style=for-the-badge)](https://redis.io/docs/)
[![PostreSQL](https://img.shields.io/badge/PostreSQL-12.12-green?style=for-the-badge)](https://www.postgresql.org/docs/)

We are using Jira for Kanban board:

[Link to the board](https://coaxpythonbootcamp.atlassian.net/jira/software/projects/CPB/boards/1)

## Runtime Environment

Environmental data is set up via .ENV files, that should have the following info:

```env
DJANGO_SETTINGS_MODULE=config.settings
PROJECT_NAME=
SITE_URL=
SECRET_KEY=
ALLOWED_HOSTS=*
CORS_ALLOW_ALL_ORIGINS=YES
EMAIL_BACKEND=
DEFAULT_FROM_EMAIL=
REDIS_URL=
EMAIL_HOST_USER =
EMAIL_HOST_PASSWORD =
DEBUG_MODE=YES
```

## Commands

```bash
# Run to create migrations
python manage.py makemigrations

# Run apply migrations
python manage.py migrate

# Collect static into Storage
python manage.py collectstatic --no-input

# Create superuser
python manage.py createsuperuser

# To enter interactive Django shell
python manage.py shell

# To run a development server
python manage.py runserver

# To run a celery worker
celery -A config.celery worker --loginfo=info
```

## Development Environment

In order to test this project on your local machine, do the following:

- Clone this repo to your local machine using the following command:

```bash
git clone https://github.com/DevIhor/Recruiter.git
```

- Navigate into the folder and install the requirements by running the following command:

```bash
cd Recruiter && pip install -r requirements/dev.txt
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
coverage run -m pytest
coverage report
```

## Deployment instructions

Live server is available at [this link](http://65.109.3.1/swagger/).
