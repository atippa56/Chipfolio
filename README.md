# Bankroll Tracker

A comprehensive poker session tracking application built with FastAPI (Python) backend and React (TypeScript) frontend. Track your poker sessions, analyze profits, and visualize your bankroll progression over time.

## ✨ Features

- **Session Management**: Create, view, edit, and delete poker sessions
- **Profit Tracking**: Automatic calculation of net profit and big blinds per hour
- **Interactive Charts**: Cumulative profit visualization with Recharts
- **Separate Blind Inputs**: Individual small blind and big blind fields for accuracy
- **Responsive Design**: Clean, modern UI that works on all devices
- **Real-time Updates**: Live data synchronization between frontend and backend
- **Comprehensive Testing**: Full test coverage for backend API endpoints

## 🏗️ Architecture

### Backend (FastAPI + SQLAlchemy)
- **FastAPI**: Modern, fast Python web framework
- **SQLAlchemy**: Powerful SQL toolkit and ORM
- **SQLite**: Lightweight, file-based database
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: Lightning-fast ASGI server

### Frontend (React + TypeScript)
- **React 18**: Modern UI library with hooks
- **TypeScript**: Type-safe JavaScript for better development
- **Recharts**: Beautiful, responsive charts for data visualization
- **CSS Modules**: Scoped styling without conflicts
- **Error Boundaries**: Robust error handling

### Optional Desktop App (Tauri)
- **Rust**: High-performance, memory-safe systems programming
- **Tauri**: Build smaller, faster, and more secure desktop applications
- **Cross-platform**: Windows, macOS, and Linux support

## 🚀 Quick Start

### Prerequisites
- **Python 3.9+** with pip
- **Node.js 18+** with npm
- **Git** for version control

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Bankroll
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

### 3. Frontend Setup
```bash
cd frontend
npm install
```

### 4. Start Development Services

#### Terminal 1 - Backend API
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

#### Terminal 2 - Frontend Application
```bash
cd frontend
npm start
```

### 5. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📖 Usage

### Adding a Session
1. Fill out the session form with:
   - **Date**: Session date
   - **Location**: Casino or venue name
   - **Small Blind**: Small blind amount (e.g., $1)
   - **Big Blind**: Big blind amount (e.g., $2)
   - **Buy-in**: Initial investment amount
   - **Cash Out**: Final amount when leaving
   - **Hours**: Session duration
   - **Notes**: Optional session notes

2. Click "Add Session" to save

### Viewing Sessions
- **Session List**: View all sessions in a sortable table
- **Profit Calculation**: Automatic net profit (Cash Out - Buy-in)
- **Statistics**: Total sessions, total profit, average per session
- **Chart Visualization**: Cumulative profit over time

### Managing Sessions
- **Delete**: Remove sessions with confirmation dialog
- **Real-time Updates**: Changes reflect immediately across all components

## 🧪 Testing

### Backend Tests
```bash
cd backend
python -m pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

### Test Coverage
```bash
cd backend
python -m pytest tests/ --cov=app --cov-report=html
```

## 📦 Database Schema

### Sessions Table
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| date | DateTime | Session date |
| location | String | Casino/venue name |
| sb_size | Float | Small blind amount |
| bb_size | Float | Big blind amount |
| buy_in | Float | Initial investment |
| cash_out | Float | Final amount |
| hours | Float | Session duration |
| notes | Text | Optional notes |
| created_at | DateTime | Record creation time |
| updated_at | DateTime | Last update time |

### Computed Properties
- **net_profit**: `cash_out - buy_in`
- **bb_per_hour**: `(net_profit / bb_size) / hours`

## 🔧 Development

### Project Structure
```
Bankroll/
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── database/       # Database configuration
│   │   ├── models/         # SQLAlchemy models
│   │   ├── routers/        # API route handlers
│   │   ├── schemas.py      # Pydantic schemas
│   │   └── main.py         # Application entry point
│   ├── tests/              # Backend tests
│   └── requirements.txt    # Python dependencies
├── frontend/               # React application
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── hooks/          # Custom React hooks
│   │   ├── services/       # API service layer
│   │   ├── types/          # TypeScript definitions
│   │   └── index.tsx       # Application entry point
│   └── package.json        # Node.js dependencies
├── docs/                   # Documentation
├── .github/workflows/      # CI/CD pipelines
└── tauri/                  # Desktop app configuration
```

### API Endpoints

#### Sessions
- `GET /sessions/` - List all sessions
- `POST /sessions/` - Create new session
- `GET /sessions/{id}` - Get specific session
- `PUT /sessions/{id}` - Update session
- `DELETE /sessions/{id}` - Delete session

#### Health Check
- `GET /` - API health check

### Code Quality
- **Backend Linting**: flake8, black
- **Frontend Linting**: ESLint, Prettier
- **Type Checking**: mypy (Python), TypeScript
- **Testing**: pytest (Backend), Jest (Frontend)

## 🚀 Deployment

### Development
See [Quick Start](#-quick-start) section above.

### Production
Detailed deployment instructions available in [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md):
- Traditional web deployment with nginx
- Docker containerization
- Tauri desktop application
- CI/CD with GitHub Actions

### Environment Variables
Create `.env` file in project root:
```env
# Database
DATABASE_URL=sqlite:///./bankroll.db

# Development
DEBUG=true
```

## 🔄 CI/CD Pipeline

Automated GitHub Actions pipeline includes:
- **Testing**: Backend and frontend test suites
- **Linting**: Code quality checks
- **Building**: Application builds and artifacts
- **Deployment**: Automated staging deployment
- **Cross-platform**: Tauri builds for Windows, macOS, Linux

## 🛠️ Tech Stack

### Backend
- ![Python](https://img.shields.io/badge/Python-3.9+-blue)
- ![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green)
- ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-orange)
- ![SQLite](https://img.shields.io/badge/SQLite-3.0+-lightgrey)
- ![Pydantic](https://img.shields.io/badge/Pydantic-2.0+-red)

### Frontend
- ![React](https://img.shields.io/badge/React-18+-blue)
- ![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue)
- ![Recharts](https://img.shields.io/badge/Recharts-2.8+-green)
- ![CSS3](https://img.shields.io/badge/CSS3-Modern-blue)

### Desktop (Optional)
- ![Rust](https://img.shields.io/badge/Rust-1.70+-orange)
- ![Tauri](https://img.shields.io/badge/Tauri-1.5+-yellow)

## 📊 Current Status

✅ **Completed Features (70%)**
- [x] Backend API with full CRUD operations
- [x] Frontend React application with modern UI
- [x] Session creation and management
- [x] Profit calculations and statistics
- [x] Interactive profit charts
- [x] Database schema and migrations
- [x] Comprehensive testing suite

🚧 **In Progress (30%)**
- [ ] Tauri desktop application packaging
- [ ] CI/CD pipeline implementation  
- [ ] Final documentation and deployment guides

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow existing code style and conventions
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](../../issues)
- **Discussions**: [GitHub Discussions](../../discussions)

## 🙏 Acknowledgments

- **FastAPI** for the excellent Python web framework
- **React** team for the powerful UI library
- **Recharts** for beautiful data visualization
- **Tauri** for cross-platform desktop applications
- **SQLAlchemy** for robust database ORM 