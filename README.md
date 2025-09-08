# PyGoRP - Python + Go + React + PostgreSQL Boilerplate

A modern full-stack boilerplate that serves as an alternative to the MERN stack, featuring high-performance Go backend, AI-ready Python service, beautiful React frontend with Shadcn UI, and robust PostgreSQL database.

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Next.js       │    │      Go         │    │    Python       │
│   Frontend      │◄──►│   Backend API   │◄──►│  AI/ML Service  │
│   (Port 3000)   │    │   (Port 8080)   │    │   (Port 8000)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │  PostgreSQL     │
                    │   Database      │
                    │   (Port 5432)   │
                    └─────────────────┘
```

## 🚀 Features

- **Go Backend**: High-performance REST API with Gin framework
- **Python AI Service**: FastAPI for machine learning and AI interactions
- **React Frontend**: Next.js with TypeScript and Shadcn UI components
- **PostgreSQL Database**: Robust relational database with Docker
- **Redis**: In-memory data store for caching and sessions
- **Docker**: Complete containerization for all services
- **Health Checks**: Built-in health monitoring for all services
- **CORS**: Properly configured cross-origin resource sharing

## 🛠️ Tech Stack

### Backend (Go)
- Gin Web Framework
- PostgreSQL driver (lib/pq)
- CORS middleware
- Structured logging

### AI Service (Python)
- FastAPI framework
- Pydantic for data validation
- SQLAlchemy for ORM
- JWT authentication support

### Frontend (React)
- Next.js 14 with App Router
- TypeScript
- Tailwind CSS
- Shadcn UI components
- Responsive design

### Database & Infrastructure
- PostgreSQL 15
- Redis 7
- Docker & Docker Compose
- PgAdmin for database management

## 📋 Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- Go 1.22+ (for local development)
- Python 3.12+ (for local development)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd pygorp

# Copy environment file
cp env.example .env
```

### 2. Start All Services

```bash
# Start all services with Docker Compose
docker-compose up --build

# Or run in background
docker-compose up --build -d
```

### 3. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8080
- **AI Service**: http://localhost:8000
- **PgAdmin**: http://localhost:5050 (admin@pygorp.com / admin)
- **PostgreSQL**: localhost:5432

## 🔧 Development Setup

### Local Development (Recommended for Development)

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

#### Backend
```bash
cd backend
go mod tidy
go run main.go
```

#### AI Service
```bash
cd ai-service
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

#### Database
```bash
# Start only database services
docker-compose up postgres redis pgadmin
```

## 📚 API Documentation

### Backend API (Go) - Port 8080

#### Health Check
```bash
GET /health
```

#### User Management
```bash
GET    /api/v1/users       # List all users
GET    /api/v1/users/:id   # Get user by ID
POST   /api/v1/users       # Create new user
PUT    /api/v1/users/:id   # Update user
DELETE /api/v1/users/:id   # Delete user
```

#### Request Body for Creating User
```json
{
  "name": "John Doe",
  "email": "john@example.com"
}
```

### AI Service API (Python) - Port 8000

#### Health Check
```bash
GET /health
```

#### Text Analysis
```bash
POST /api/v1/analyze/text
```

#### Request Body
```json
{
  "text": "This is a great product!",
  "analysis_type": "sentiment",
  "options": {}
}
```

#### Image Analysis
```bash
POST /api/v1/analyze/image
```

#### ML Predictions
```bash
POST /api/v1/ml/predict
```

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### AI Requests Table
```sql
CREATE TABLE ai_requests (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    request_type VARCHAR(100) NOT NULL,
    request_data JSONB,
    response_data JSONB,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE
);
```

## 🔐 Environment Variables

Create a `.env` file in the root directory:

```bash
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=password
DB_NAME=pygorp
DB_SSLMODE=disable

# Backend Configuration
PORT=8080
GIN_MODE=debug

# AI Service Configuration
AI_SERVICE_URL=http://localhost:8000
AI_SERVICE_TIMEOUT=30

# Frontend Configuration
NEXT_PUBLIC_API_URL=http://localhost:8080/api/v1
NEXT_PUBLIC_AI_SERVICE_URL=http://localhost:8000
```

## 🧪 Testing the Application

### 1. Create a User
```bash
curl -X POST http://localhost:8080/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Test User", "email": "test@example.com"}'
```

### 2. Get All Users
```bash
curl http://localhost:8080/api/v1/users
```

### 3. Test AI Service
```bash
curl -X POST http://localhost:8000/api/v1/analyze/text \
  -H "Content-Type: application/json" \
  -d '{"text": "This is amazing!", "analysis_type": "sentiment"}'
```

## 🏗️ Project Structure

```
pygorp/
├── backend/              # Go backend service
│   ├── main.go          # Main application
│   ├── go.mod           # Go modules
│   ├── Dockerfile       # Docker configuration
│   └── internal/        # Internal packages
│       ├── database/    # Database connection
│       ├── handlers/    # HTTP handlers
│       └── models/      # Data models
├── frontend/            # Next.js frontend
│   ├── src/
│   │   ├── app/         # Next.js app router
│   │   ├── components/  # React components
│   │   └── lib/         # Utilities
│   ├── Dockerfile       # Docker configuration
│   └── package.json     # Dependencies
├── ai-service/          # Python AI service
│   ├── main.py          # FastAPI application
│   ├── requirements.txt # Python dependencies
│   ├── Dockerfile       # Docker configuration
│   └── venv/            # Virtual environment
├── docker/              # Docker configurations
│   ├── init.sql         # Database initialization
│   └── .env             # Environment variables
├── docker-compose.yml   # Docker Compose orchestration
└── README.md           # This file
```

## 🔧 Customization

### Adding New API Endpoints

#### Backend (Go)
1. Add new model in `internal/models/`
2. Create handler in `internal/handlers/`
3. Register route in `main.go`

#### AI Service (Python)
1. Add new endpoint in `main.py`
2. Implement your ML logic
3. Update API documentation

### Frontend Components
1. Use Shadcn CLI to add new components
2. Follow the existing component structure
3. Ensure TypeScript types are properly defined

## 🚦 Monitoring & Health Checks

All services include health check endpoints:

- Backend: `GET /health`
- AI Service: `GET /health`
- Database: Built-in PostgreSQL health checks
- Redis: Built-in Redis health checks

## 📈 Scaling Considerations

### Horizontal Scaling
- Go backend is stateless and can be scaled horizontally
- AI service can be scaled based on ML workload
- Use Redis for session management and caching
- Consider using a load balancer for multiple instances

### Database Scaling
- PostgreSQL can be scaled with read replicas
- Consider connection pooling for high traffic
- Use database indexes for optimal performance

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙋 Support

If you have any questions or need help:

1. Check the API documentation
2. Review the code comments
3. Create an issue in the repository
4. Check the troubleshooting section below

## 🔧 Troubleshooting

### Common Issues

#### Docker Issues
```bash
# Stop all services
docker-compose down

# Remove volumes (WARNING: This deletes database data)
docker-compose down -v

# Rebuild and start
docker-compose up --build
```

#### Port Conflicts
If ports are already in use, modify the ports in `docker-compose.yml`:
```yaml
ports:
  - "3001:3000"  # Change host port from 3000 to 3001
```

#### Database Connection Issues
1. Ensure PostgreSQL container is running
2. Check environment variables in `.env`
3. Verify database credentials

#### Frontend Build Issues
```bash
cd frontend
rm -rf node_modules .next
npm install
npm run build
```

---

**Happy coding with PyGoRP! 🚀**
