# DevSearch: Django Course Project

A Django project built while following Dennis Ivy's 10-hour Django course. It covers Django fundamentals, building a REST API with Django REST Framework (DRF), and connecting to a separate front end using CORS. A mock front end is included to demonstrate the API in action.


## Table of Contents

- [Overview](#overview)
- [What This Project Covers](#what-this-project-covers)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Running the Mock Front End](#running-the-mock-front-end)
- [API Overview](#api-overview)
- [CORS Configuration](#cors-configuration)
- [What I Learned](#what-i-learned)
- [Credits](#credits)

## Overview

DevSearch starts as a traditional server-rendered Django app and then adds a REST API on top, so the same backend can serve both templates and a separate front end.

The repository has two parts:

1. **`devsearch/`**: the Django backend, including the REST API built with Django REST Framework.
2. **`frontend/`**: a mock front end that consumes the API to show how a decoupled client talks to the backend across origins.

## What This Project Covers

### Django fundamentals
- Project and app structure, settings, and the request/response cycle
- URL routing, including dynamic URL parameters
- Views and context data
- Templates, template inheritance, and template tags
- Static and media file handling
- Models, migrations, and the ORM
- The Django admin
- Forms and ModelForms
- User authentication
- Search and pagination

### REST API development
- Django REST Framework setup and configuration
- Serializers
- API views and routes
- CRUD operations over HTTP
- Authentication and permissions for API access

### Connecting to a front end
- Cross-Origin Resource Sharing (CORS) with `django-cors-headers`
- Consuming the API from a separate front end on a different origin

## Tech Stack

- Python 3
- Django
- Django REST Framework
- django-cors-headers
- SQLite (default development database)
- Mock front end in `frontend/`

## Project Structure

```
DevSearch-Django-APP/
├── devsearch/     # Django backend (project, apps, API)
├── frontend/      # Mock front end that consumes the API
└── README.md
```

## API Overview

Base URL: `http://127.0.0.1:8000/api/`

| Method | Endpoint                | Description          |
|--------|-------------------------|----------------------|
| GET    | `/api/projects/`        | List all projects    |
| GET    | `/api/projects/<id>/`   | Retrieve one project |


Protected endpoints require an `Authorization` header with your credentials or token.

## CORS Configuration

Cross-origin requests from the front end are enabled with `django-cors-headers`.

```python
# settings.py
INSTALLED_APPS = [
    # ...
    "corsheaders",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # Place as high as possible
    "django.middleware.common.CommonMiddleware",
    # ...
]

# Allow only the front end origins you trust
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]
```

## What I Learned

- How Django's MVT architecture fits together, from URLs to templates
- Modeling data and querying it through the ORM
- Building authentication flows
- Turning a Django app into a REST API with serializers and API views
- How browsers enforce the same-origin policy and how CORS safely relaxes it
- Separating a backend from a front end and wiring them together