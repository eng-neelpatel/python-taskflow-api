# TaskFlow API

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)
![Code Style](https://img.shields.io/badge/Code%20Style-Black-black.svg)

A production-ready REST API built with FastAPI, demonstrating clean architecture, industry best practices, and modern Python development patterns.

## Skills Demonstrated

This project showcases proficiency in:

- **Backend Development** - RESTful API design with FastAPI
- **Database Design** - SQLAlchemy ORM, migrations, relationships
- **Authentication** - JWT-based authentication & authorization
- **Testing** - Unit tests with pytest and test coverage
- **Clean Architecture** - SOLID principles, dependency injection
- **DevOps** - Docker containerization, CI/CD ready
- **Documentation** - OpenAPI/Swagger auto-generated docs

## Tech Stack

| Category | Technology |
|----------|------------|
| Framework | FastAPI |
| Database | PostgreSQL + SQLAlchemy |
| Authentication | JWT (python-jose) |
| Validation | Pydantic |
| Testing | pytest + TestClient |
| Documentation | OpenAPI/Swagger |
| Containerization | Docker |

## Project Structure

```
python-taskflow-api/
|-- app/
|   |-- main.py              # Application entry point
|   |-- api/
|   |   |-- v1/              # API version 1 routes
|   |-- core/
|   |   |-- config.py        # Configuration settings
|   |   |-- database.py      # Database connection
|   |   |-- security.py      # Auth utilities
|   |-- models/
|   |   |-- task.py          # Task SQLAlchemy model
|   |   |-- user.py          # User model
|   |-- schemas/             # Pydantic schemas
|   |-- services/            # Business logic
|   |-- middleware/          # Custom middleware
|-- tests/
|   |-- test_tasks.py        # API & model tests
|-- requirements.txt
|-- Dockerfile
|-- docker-compose.yml
```

## Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL (or SQLite for development)

### Installation

```bash
# Clone the repository
git clone https://github.com/eng-neelpatel/python-taskflow-api.git
cd python-taskflow-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --reload
```

### API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register new user |
| POST | `/api/v1/auth/login` | Login & get token |
| POST | `/api/v1/auth/refresh` | Refresh access token |

### Tasks
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/tasks` | List all tasks |
| POST | `/api/v1/tasks` | Create new task |
| GET | `/api/v1/tasks/{id}` | Get task by ID |
| PUT | `/api/v1/tasks/{id}` | Update task |
| DELETE | `/api/v1/tasks/{id}` | Delete task |

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_tasks.py -v
```

## Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Run in detached mode
docker-compose up -d
```

## Environment Variables

```env
DATABASE_URL=postgresql://user:pass@localhost/taskflow
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Author

**Neel Patel**
- GitHub: [@eng-neelpatel](https://github.com/eng-neelpatel)
- LinkedIn: [Neel Patel](https://linkedin.com/in/your-profile)

## License

This project is licensed under the MIT License.

---

Built with FastAPI and SQLAlchemy | Demonstrating production-ready Python development
