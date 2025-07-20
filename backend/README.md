# Internal Feedback Tool - Backend API

A FastAPI-based backend for structured feedback sharing between managers and team members.

## Features

- **Role-based Authentication**: JWT-based auth with Manager/Employee roles
- **Team Management**: Managers can only see their team members
- **Structured Feedback**: Strengths, areas to improve, sentiment tracking
- **Feedback History**: Complete timeline with acknowledgment system
- **Dashboard Analytics**: Role-specific dashboards with stats
- **Employee Comments**: Employees can respond to feedback

## Tech Stack

- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **SQLite** - Database (easily switchable to PostgreSQL)
- **JWT** - Token-based authentication
- **Pydantic** - Data validation and serialization

## Quick Start

### Using Docker (Recommended)

```bash
# Build and run the container
docker build -t feedback-tool-backend .
docker run -p 8000:8000 feedback-tool-backend
```

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit:
- **Interactive API Docs**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Core Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token

### Users
- `GET /users/me` - Get current user profile
- `GET /users/team` - Get team members (managers only)
- `GET /users/{user_id}` - Get user profile (with access control)

### Feedback
- `POST /feedback/` - Create feedback (managers only)
- `GET /feedback/my-feedback` - Get user's feedback
- `GET /feedback/employee/{employee_id}` - Get employee feedback
- `PUT /feedback/{feedback_id}` - Update feedback (managers only)
- `POST /feedback/{feedback_id}/acknowledge` - Acknowledge feedback
- `POST /feedback/{feedback_id}/comment` - Add employee comment

### Dashboard
- `GET /dashboard/manager` - Manager dashboard with team stats
- `GET /dashboard/employee` - Employee dashboard with feedback timeline

## Database Schema

### User Model
- `id`, `name`, `email`, `password_hash`
- `role` (manager/employee)
- `manager_id` (for employees)
- Self-referencing relationship for team hierarchy

### Feedback Model
- `id`, `employee_id`, `manager_id`
- `strengths`, `areas_to_improve`, `sentiment`
- `acknowledged`, `acknowledged_at`
- `tags`, `is_anonymous`, `employee_comment`
- Timestamps for creation and updates

## Example Usage

### 1. Register Users
```bash
# Register a manager
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Manager",
    "email": "john@company.com",
    "password": "password123",
    "role": "manager"
  }'

# Register an employee
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Employee",
    "email": "jane@company.com",
    "password": "password123",
    "role": "employee",
    "manager_id": 1
  }'
```

### 2. Login and Get Token
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john@company.com&password=password123"
```

### 3. Create Feedback
```bash
curl -X POST "http://localhost:8000/feedback/" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": 2,
    "strengths": "Great communication skills and proactive approach",
    "areas_to_improve": "Could benefit from more technical depth in presentations",
    "sentiment": "positive",
    "tags": "communication,presentation"
  }'
```

## Security Features

- Password hashing with bcrypt
- JWT token authentication
- Role-based access control
- Team-based data isolation
- Input validation with Pydantic

## Development

### Project Structure
```
backend/
├── app/
│   ├── main.py          # FastAPI application
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   ├── database.py      # DB configuration
│   ├── auth.py          # Authentication logic
│   ├── crud.py          # Database operations
│   └── routers/         # API route handlers
├── Dockerfile
├── requirements.txt
└── README.md
```

### Environment Variables
Create a `.env` file for production:
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./feedback_tool.db
```

## Deployment

The application includes a Dockerfile for easy deployment to any container platform:
- Render
- Railway
- Heroku
- AWS ECS
- Google Cloud Run

## Next Steps

1. **Frontend Integration**: Connect with React/Vue/Svelte frontend
2. **Email Notifications**: Add email alerts for new feedback
3. **Advanced Analytics**: More detailed dashboard metrics
4. **File Uploads**: Support for feedback attachments
5. **PostgreSQL**: Switch to PostgreSQL for production