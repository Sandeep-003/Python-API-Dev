# Python API Auth Service

This project is a small but complete authentication and posts API built with **FastAPI**, **SQLAlchemy**, **PostgreSQL**, and **JWT (JSON Web Tokens)**. It demonstrates how to build a secure backend for user registration, login, protected resources, and simple voting on posts.

---

## Features

- User registration with hashed passwords (using `passlib` / bcrypt)
- Login with username + password to obtain a JWT access token
- OAuth2 password flow with bearer token (`Authorization: Bearer <token>`)
- Protected routes requiring authentication
- CRUD operations for posts (scoped to the logged‑in user)
- Simple vote model (user ↔ post) prepared in the database layer
- PostgreSQL integration via SQLAlchemy ORM
- Alembic migrations for schema evolution
- Interactive API docs via Swagger UI and ReDoc

---

## Tech Stack

- **Language**: Python 3.x
- **Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Database**: PostgreSQL
- **Auth**: OAuth2 + JWT (`python-jose`)
- **Password hashing**: `passlib[bcrypt]`
- **Migrations**: Alembic

Main entrypoint: `main.py` (FastAPI app with included routers).

---

## Project Structure

```text
.
├── main.py          # FastAPI application instance, includes routers
├── database.py      # SQLAlchemy engine and DB session (`get_db` dependency)
├── model.py         # SQLAlchemy ORM models (Users, Posts, Votes)
├── schema.py        # Pydantic models (request/response schemas, tokens, votes)
├── users.py         # `/users` router – user registration
├── auth.py          # `/login` route – authentication and token generation
├── OAuth2.py        # JWT creation/verification, `get_current_user` dependency
├── posts.py         # `/posts` router – CRUD operations for posts
├── utils.py         # Password hashing / verification helpers
├── alembic.ini      # Alembic configuration
└── alembic/         # Alembic env and migration versions
```

---

## Requirements

Create and activate a virtual environment, then install the required packages. A typical `requirements.txt` for this project would include:

```text
fastapi
uvicorn[standard]
SQLAlchemy
psycopg2-binary
python-jose[cryptography]
passlib[bcrypt]
pydantic
alembic
python-dotenv  # optional, if you move secrets/URL to env vars
```

Install dependencies (from the project root):

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

> If you don’t have a `requirements.txt` yet, you can create one with the list above and then run `pip install -r requirements.txt`.

---

## Database Configuration

The database connection string is defined in `database.py`:

```python
SQL_ALCHEMY_DB_URL = 'postgresql://postgres:lunar@localhost/pyapp'
```

1. Ensure PostgreSQL is installed and running.
2. Create a database named `pyapp` (or adjust the URL to match your actual database name, username, and password):

```powershell
psql -U postgres -c "CREATE DATABASE pyapp;"
```

3. (Optional but recommended) Move the URL and other secrets (like `SECRET_KEY` in `OAuth2.py`) to environment variables or a `.env` file for production use.

---

## Running Database Migrations (Alembic)

Alembic is already configured in the `alembic/` directory with versions under `alembic/versions/`.

Typical workflow:

```powershell
.venv\Scripts\activate
alembic upgrade head
```

- `alembic upgrade head` applies all migrations under `alembic/versions` to bring the database schema up-to-date (creating `users`, `posts`, `votes`, etc.).
- If you later modify models, you can generate new migrations (depending on how Alembic is configured in `alembic/env.py`).

---

## Running the Application

From the project root (`Auth` folder):

```powershell
.venv\Scripts\activate
uvicorn main:app --reload
```

- The `--reload` flag enables auto‑reload during development.
- By default, Uvicorn will serve on `http://127.0.0.1:8000`.

**API docs:**
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

---

## Authentication Flow

### 1. Register a User

**Endpoint**: `POST /users/`

**Body (JSON)** – matches `schema.UserCreate`:

```json
{
  "user_id": "alice",
  "email": "alice@example.com",
  "password": "strong_password"
}
```

- Passwords are hashed using `utils.hash` before being stored.
- On success, you receive the created user (with hashed password in the DB).

### 2. Login and Get Token

**Endpoint**: `POST /login/`

- Uses `OAuth2PasswordRequestForm` (form data, not JSON).
- Example request body (as `application/x-www-form-urlencoded`):

```text
username=alice&password=strong_password
```

**Response** (matches `schema.Token`):

```json
{
  "access_token": "<JWT_TOKEN>",
  "token_type": "bearer"
}
```

### 3. Call Protected Endpoints

Include the token from the login step in the `Authorization` header:

```http
Authorization: Bearer <JWT_TOKEN>
```

The `OAuth2.get_current_user` dependency:
- Extracts the token via `OAuth2PasswordBearer`.
- Verifies and decodes it (`create_access_token`, `decode_access_token`, `verify_token`).
- Fetches the corresponding `Users` record from the database.
- Injects the `current_user` object into routes that depend on it.

If validation fails, FastAPI returns `401 Unauthorized` with `"Could not validate credentials"`.

---

## Posts Endpoints

All `/posts` endpoints are protected by `dependencies=[Depends(OAuth2.get_current_user)]` in `posts.py`.

### Get All Posts for Current User

- **Endpoint**: `GET /posts/all/`
- **Auth**: Required.
- **Response**: `list[schema.PostResponse]` – all posts that belong to the current user.

### Get Single Post by ID

- **Endpoint**: `GET /posts/{post_id}/`
- **Auth**: Required.
- **Response**: `schema.PostResponse`.
- Returns 404 if the post does not exist or does not belong to the current user.

### Create Post

- **Endpoint**: `POST /posts/`
- **Auth**: Required.
- **Body (JSON)** – matches `schema.PostCreate`:

```json
{
  "post_id": 1,
  "post_data": "My first post!",
  "user_id": "ignored_on_server_side"
}
```

> Note: On the server side, `user_id` is overridden with `current_user.user_id`.

### Update Post

- **Endpoint**: `PUT /posts/{post_id}/`
- **Auth**: Required.
- **Body (JSON)**: `schema.PostCreate` (the `post_data` field is used; `user_id` is re‑set to the current user).
- Checks that the post exists and that it belongs to the current user before updating.

### Delete Post

- **Endpoint**: `DELETE /posts/{post_id}`
- **Auth**: Required.
- Returns `204 No Content` on successful deletion.
- Returns 404 if the post does not exist, or 403 if it belongs to another user.

---

## Data Models Overview

### Database Models (`model.py`)

- `Users`
  - `user_id: String` (primary key)
  - `email: String` (unique)
  - `password: String` (hashed)
  - `created_at: TIMESTAMP` (server default `now()`)

- `Posts`
  - `post_id: Integer` (primary key, autoincrement)
  - `post_data: String`
  - `created_at: TIMESTAMP` (server default `now()`)
  - `user_id: String` (FK to `users.user_id`)

- `Votes`
  - Composite primary key: (`user_id`, `post_id`)
  - FKs to `users.user_id` and `posts.post_id`

### Pydantic Schemas (`schema.py`)

- `UserCreate`, `UserResponse` – for creating and returning users.
- `PostCreate`, `PostResponse` – for posts.
- `Token`, `TokenData`, `UserLogin` – for auth.
- `Vote` – for vote request body.

All response schemas that map to ORM models use `Config.from_attributes = True` so they can be created from SQLAlchemy objects.

---

## Security Notes

- **Secret key**: `SECRET_KEY` in `OAuth2.py` is currently hard‑coded and should be moved to environment variables for any real deployment.
- **Token lifetime**: `ACCESS_TOKEN_EXPIRE_MINUTES = 10` – short‑lived tokens for improved security.
- **Password storage**: Uses bcrypt hashing via `passlib.context.CryptContext`.
- For production, consider:
  - HTTPS termination (e.g., via reverse proxy like Nginx or a cloud provider).
  - Refresh tokens or re‑login flows.
  - Role/permission system on top of the basic user model.

---

## Development Tips

- Use the interactive docs (`/docs`) to try out endpoints quickly.
- When experimenting with routes that use `OAuth2PasswordRequestForm`, remember to send form data (not JSON).
- For repeated manual testing, tools like Postman or VS Code REST Client are handy; set a collection variable for the bearer token.
- To extend the project, you can:
  - Add routes for password reset / change.
  - Implement listing and casting votes using the `Votes` model.
  - Add pagination or filtering for posts.

---

## Running Tests (If Added)

At the moment, there are no automated tests included in the repository. A typical pattern for FastAPI would be to use `pytest` plus `httpx` or `fastapi.testclient`. Once tests exist, you can run them with:

```powershell
pytest
```

---

## Summary

This project serves as a compact reference for building an authenticated REST API using FastAPI, PostgreSQL, SQLAlchemy, and JWT. It covers the full flow from user registration and login, through token‑based authentication, to protected CRUD operations on user‑owned resources. Use it as a learning project or as a starting point for a more advanced backend service.
