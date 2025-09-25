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
Add users & catalog apps, JWT auth endpoints, product discovery filters, and Swagger UI at `/api/docs`.

# alx-project-nexus