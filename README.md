# Wedding Planner - Full Stack Application

A comprehensive wedding planning application with separate admin dashboard and guest registration portal.

## 🎯 Overview

This application provides two main interfaces:

### 1. Admin/Planning Dashboard
- **Analytics & Insights**: View registration statistics, guest attendance, dietary requirements
- **Content Management**: Manage registration page content, wedding details, FAQs
- **Task Management**: Organize wedding planning tasks with priorities and due dates
- **Cost Estimation**: Track and manage wedding budget and expenses
- **Request Management**: Handle RSVPs, special requests, and guest communications
- **Guest Management**: View and manage all guest information

### 2. Guest Registration Portal
- **RSVP Registration**: Simple and intuitive registration form
- **Guest Information**: Collect names, contact details, dietary restrictions
- **Wedding Information**: Access to wedding details, schedule, venue information
- **Personal Dashboard**: View RSVP status and update information

## 🏗️ Architecture

### Backend (Flask)
- **Framework**: Flask with SQLAlchemy ORM
- **Database**: PostgreSQL (production) / SQLite (development)
- **Authentication**: JWT with Flask-JWT-Extended
- **API**: RESTful API with role-based access control
- **Deployment**: Render

### Frontend (React)
- **Framework**: React 19 with Vite
- **UI Library**: shadcn/ui with Tailwind CSS
- **State Management**: React Query for server state
- **Routing**: React Router with protected routes
- **Deployment**: Vercel

## 📁 Project Structure

```
wedding-planner/
├── wedding-planner-backend/     # Flask API server
│   ├── src/
│   │   ├── models/              # Database models
│   │   ├── routes/              # API endpoints
│   │   ├── services/            # Business logic
│   │   └── main.py             # Application entry point
│   ├── venv/                   # Python virtual environment
│   └── requirements.txt        # Python dependencies
├── wedding-planner-frontend/    # React application
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── pages/              # Page components
│   │   │   ├── admin/         # Admin dashboard pages
│   │   │   └── guest/         # Guest portal pages
│   │   ├── hooks/              # Custom hooks
│   │   ├── lib/                # Utilities and API client
│   │   └── App.jsx            # Main application component
│   └── package.json           # Node.js dependencies
└── README.md                  # This file
```

## 🛠️ Development Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- pnpm (recommended) or npm

### Backend Setup

```bash
cd wedding-planner-backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python src/main.py
```

### Frontend Setup

```bash
cd wedding-planner-frontend
pnpm install
pnpm run dev
```

### Environment Variables

#### Backend (.env)

```env
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here
DATABASE_URL=postgresql://user:password@host:port/database  # For production
FRONTEND_URL=http://localhost:5173  # For development, use production URL in production
```

#### Frontend (.env.local)

```env
VITE_API_URL=http://localhost:5000/api  # For development
```

## 🚀 Deployment

### Backend (Render)

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Set build command: `pip install -r wedding-planner-backend/requirements.txt`
4. Set start command: `cd wedding-planner-backend && python src/main.py`
5. Add environment variables (DATABASE_URL, SECRET_KEY, JWT_SECRET_KEY, FRONTEND_URL)

### Frontend (Vercel)

1. Connect your GitHub repository to Vercel
2. Set root directory to `wedding-planner-frontend`
3. Build command: `pnpm run build`
4. Output directory: `dist`
5. Add environment variables (VITE_API_URL)

### Database (Render PostgreSQL)

1. Create a PostgreSQL database on Render
2. Copy the connection string to your backend environment variables

## 📚 API Endpoints (Planned)

### Authentication
- `POST /api/auth/register` - Admin registration
- `POST /api/auth/login` - Admin login
- `POST /api/auth/refresh` - Token refresh
- `GET /api/auth/profile` - Get user profile

### Guests
- `GET /api/guests` - Get all guests (admin)
- `POST /api/guests/register` - Guest registration (public)
- `GET /api/guests/:id` - Get guest details
- `PUT /api/guests/:id` - Update guest information
- `DELETE /api/guests/:id` - Delete guest (admin)

### Tasks
- `GET /api/tasks` - Get all tasks
- `POST /api/tasks` - Create task
- `PUT /api/tasks/:id` - Update task
- `DELETE /api/tasks/:id` - Delete task

### Costs
- `GET /api/costs` - Get all cost items
- `POST /api/costs` - Add cost item
- `PUT /api/costs/:id` - Update cost item
- `DELETE /api/costs/:id` - Delete cost item

### Content
- `GET /api/content` - Get public content
- `PUT /api/content` - Update content (admin)

### Analytics
- `GET /api/analytics/overview` - Get registration overview
- `GET /api/analytics/dietary` - Get dietary requirements summary
- `GET /api/analytics/attendance` - Get attendance statistics

## 🔒 Security Features

- **Password Security**: Bcrypt hashing with salt
- **JWT Authentication**: Secure token-based authentication for admin
- **Role-Based Access**: Admin vs Guest access control
- **CORS Protection**: Configured for specific origins
- **Input Validation**: Comprehensive server-side validation
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection

## 📄 License

This project is licensed under the MIT License.

