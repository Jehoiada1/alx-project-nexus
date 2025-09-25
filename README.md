## E-Commerce Backend (Django + PostgreSQL + JWT + Swagger)

Production-style backend providing product & category management, user authentication, and API documentation.

### Stack
* Django / Django REST Framework
* PostgreSQL
* JWT auth (SimpleJWT)
* drf-spectacular (OpenAPI/Swagger)
* docker-compose for local dev

### Initial Setup (Without Docker)
1. Create & activate virtual environment
2. Install dependencies:
	`pip install -r requirements.txt`
3. Copy environment file:
	`copy .env.example .env` (Windows) or `cp .env.example .env` (Linux/macOS)
4. Update `.env` values (SECRET_KEY, DB, etc.).
5. Run migrations: `python manage.py migrate`
6. Create superuser: `python manage.py createsuperuser`
7. Start server: `python manage.py runserver`

### Docker
`docker compose up --build`

### Production (Gunicorn + WhiteNoise)
Build image (still uses dev CMD by default). For production run:

1. Set environment (DEBUG=False, proper ALLOWED_HOSTS).  
2. Collect static & run Gunicorn (example command):

```
python manage.py collectstatic --noinput
gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 3 --access-logfile - --error-logfile -
```

Or override Docker CMD:

```
docker run --env-file .env -e DEBUG=False -p 8000:8000 \
	--name ecommerce api-image \
	sh -c "./docker-entrypoint.sh gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 3"
```

Health check endpoint: `GET /health/` returns `{ "status": "ok" }`.

### CI
GitHub Actions workflow at `.github/workflows/ci.yml` runs migrations & tests against Postgres.

### Roadmap / Commits
Planned commit messages:
1. feat: set up Django project with PostgreSQL
2. feat: implement JWT user authentication
3. feat: add product/category CRUD APIs
4. feat: implement filtering, sorting, pagination
5. feat: integrate Swagger/OpenAPI documentation
6. perf: optimize queries and add database indexing
7. docs: add API usage instructions in Swagger

### Next Steps
Implemented: base project, JWT auth, catalog (products & categories), filtering, sorting, pagination, Swagger UI at `/api/docs`.

### API Summary
Auth:
* POST /api/auth/register/
* POST /api/auth/login/ (obtain pair)
* POST /api/auth/refresh/
* POST /api/auth/logout/
* GET/PATCH /api/auth/me/

Catalog:
* GET /api/categories/
* POST /api/categories/
* GET /api/categories/{id}/
* PUT/PATCH /api/categories/{id}/
* DELETE /api/categories/{id}/
* GET /api/products/?category=1&min_price=10&max_price=50&search=shirt&ordering=price&page=1&page_size=20
* POST /api/products/
* GET /api/products/{id}/
* PUT/PATCH /api/products/{id}/
* DELETE /api/products/{id}/

Docs:
* /api/schema/ (raw OpenAPI JSON)
* /api/docs/ (Swagger UI)

### Filtering & Sorting
Query params for products:
* category: category id
* min_price / max_price
* search: keyword in name or description
* ordering: price, -price, created_at, -created_at
* page, page_size (max 100)

### Performance
* select_related(category) on product queries
* DB indexes on (category, price), price, created_at
* Paginated responses

### Remaining Enhancements
* Add rate limiting / caching layer
* Add ordering & inventory events
* Add unit tests & CI workflow
* Deployment config (Gunicorn + Nginx) / production Dockerfile stage


# alx-project-nexus