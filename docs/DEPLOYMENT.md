# Bankroll Tracker - Deployment Guide

This guide covers deploying the Bankroll Tracker application in various environments.

## Architecture Overview

The Bankroll Tracker is a full-stack application with three components:
- **Backend**: FastAPI Python application with SQLite database
- **Frontend**: React TypeScript application with modern UI components
- **Desktop App**: Tauri-based native application (optional)

## Prerequisites

### Backend Requirements
- Python 3.9+
- pip package manager
- SQLite (included with Python)

### Frontend Requirements  
- Node.js 18+
- npm package manager

### Desktop App Requirements (Optional)
- Rust toolchain
- Platform-specific dependencies:
  - **Linux**: libgtk-3-dev, libwebkit2gtk-4.0-dev, libappindicator3-dev
  - **macOS**: Xcode Command Line Tools
  - **Windows**: Microsoft Visual Studio C++ Build Tools

## Development Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd Bankroll
```

### 2. Backend Setup
```bash
cd backend
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Frontend Setup
```bash
cd frontend
npm install
```

### 4. Environment Configuration
Create `.env` file in project root:
```env
# Database configuration
DATABASE_URL=sqlite:///./bankroll.db

# Development settings
DEBUG=true
```

## Running in Development

### Start Backend (Terminal 1)
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

### Start Frontend (Terminal 2)
```bash
cd frontend
npm start
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Production Deployment

### Option 1: Traditional Web Deployment

#### Backend (using Gunicorn)
```bash
cd backend
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

#### Frontend (build and serve)
```bash
cd frontend
npm run build
# Serve the build directory with nginx/apache or a static file server
```

#### Nginx Configuration Example
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        root /path/to/frontend/build;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Option 2: Docker Deployment

#### Backend Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Frontend Dockerfile
```dockerfile
FROM node:18-alpine as build

WORKDIR /app
COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
```

#### Docker Compose
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
    environment:
      - DATABASE_URL=sqlite:///./data/bankroll.db

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
```

### Option 3: Tauri Desktop Application

#### Prerequisites
Install Rust:
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs/ | sh
```

#### Setup Tauri
```bash
# Install Tauri CLI
cargo install tauri-cli

# Initialize Tauri in the project
npm install @tauri-apps/cli
```

#### Build Desktop App
```bash
cd frontend
npm run tauri build
```

The built application will be in `src-tauri/target/release/bundle/`.

## Database Migrations

### Initial Setup
The application automatically creates tables on first run.

### Manual Migration
If needed, create database manually:
```bash
cd backend
python -c "
from app.database.database import engine, Base
Base.metadata.create_all(bind=engine)
print('Database tables created')
"
```

## Environment Variables

### Production Environment Variables
```env
# Database
DATABASE_URL=sqlite:///./data/bankroll.db

# Security
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=your-domain.com,localhost

# Performance
WORKERS=4
MAX_REQUESTS=1000

# Logging
LOG_LEVEL=INFO
```

## Health Checks

### Backend Health Check
```bash
curl http://localhost:8000/
```
Expected response: `{"message":"Bankroll Tracker API is running"}`

### Frontend Health Check
Frontend serves properly when the React app loads without errors.

## Backup and Recovery

### Database Backup
```bash
cp backend/bankroll.db backup/bankroll_$(date +%Y%m%d_%H%M%S).db
```

### Automated Backup Script
```bash
#!/bin/bash
BACKUP_DIR="/path/to/backups"
DB_PATH="/path/to/bankroll.db"
DATE=$(date +%Y%m%d_%H%M%S)

cp "$DB_PATH" "$BACKUP_DIR/bankroll_$DATE.db"
find "$BACKUP_DIR" -name "bankroll_*.db" -mtime +7 -delete
```

## Monitoring

### Key Metrics to Monitor
- Backend response times
- Database size and performance
- Frontend load times
- Error rates in logs

### Log Locations
- Backend: stdout/stderr or configured log files
- Frontend: Browser console and network requests
- Web server: nginx/apache access and error logs

## Troubleshooting

### Common Issues

#### Backend won't start
1. Check Python version compatibility
2. Verify all dependencies are installed
3. Check database file permissions
4. Review error logs

#### Frontend build fails
1. Clear node_modules and reinstall: `rm -rf node_modules package-lock.json && npm install`
2. Check Node.js version compatibility
3. Verify all dependencies are available

#### Database errors
1. Check database file permissions
2. Verify SQLite is properly installed
3. Review migration scripts if custom changes were made

#### Tauri build fails
1. Ensure Rust is properly installed
2. Install platform-specific dependencies
3. Check that frontend builds successfully first

## Security Considerations

### Production Security Checklist
- [ ] Use HTTPS in production
- [ ] Set secure environment variables
- [ ] Configure proper CORS policies
- [ ] Implement rate limiting
- [ ] Regular security updates
- [ ] Database access controls
- [ ] Secure file permissions

### CORS Configuration
In production, update backend CORS settings:
```python
# In app/main.py
origins = [
    "https://your-domain.com",
    "https://www.your-domain.com",
]
```

## Performance Optimization

### Backend Optimization
- Use connection pooling for databases
- Implement caching for frequently accessed data
- Optimize database queries
- Use async/await properly

### Frontend Optimization
- Enable gzip compression
- Use CDN for static assets
- Implement code splitting
- Optimize images and assets

### Database Optimization
- Regular VACUUM operations for SQLite
- Index frequently queried columns
- Monitor and optimize slow queries

## Scaling Considerations

### Horizontal Scaling
- Load balancer in front of multiple backend instances
- Shared database or database replication
- CDN for frontend static assets

### Vertical Scaling
- Increase server resources (CPU, RAM)
- Optimize application performance
- Database performance tuning 