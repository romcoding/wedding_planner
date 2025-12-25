# Wedding Planner - Setup Summary

## 🎯 Project Overview

This is a full-stack wedding planning application with:
- **Admin Dashboard**: Complete planning cockpit for wedding organizers
- **Guest Portal**: Public registration and information site for wedding guests

## 📁 Project Structure

```
wedding-planner/
├── wedding-planner-backend/     # Flask API (deploy to Render)
│   ├── src/
│   │   ├── models/              # Database models
│   │   ├── routes/              # API endpoints
│   │   └── main.py             # Flask app entry point
│   └── requirements.txt        # Python dependencies
│
├── wedding-planner-frontend/    # React app (deploy to Vercel)
│   ├── src/
│   │   ├── pages/              # Page components
│   │   │   ├── admin/         # Admin dashboard pages
│   │   │   └── guest/         # Guest portal pages
│   │   ├── layouts/            # Layout components
│   │   ├── contexts/           # React contexts (Auth)
│   │   └── lib/                # Utilities (API client)
│   └── package.json           # Node dependencies
│
├── render.yaml                 # Render deployment config
├── vercel.json                 # Vercel deployment config
└── README.md                   # Main documentation
```

## 🚀 Deployment Architecture

### Backend → Render

**Service Type**: Web Service  
**Build Command**: `pip install -r wedding-planner-backend/requirements.txt`  
**Start Command**: `cd wedding-planner-backend && python src/main.py`  
**Database**: PostgreSQL (created separately on Render)

**Environment Variables**:
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - Flask secret key
- `JWT_SECRET_KEY` - JWT signing key
- `FRONTEND_URL` - Your Vercel deployment URL
- `PORT` - 10000 (Render default)

### Frontend → Vercel

**Framework**: Vite  
**Root Directory**: `wedding-planner-frontend`  
**Build Command**: `pnpm run build`  
**Output Directory**: `dist`

**Environment Variables**:
- `VITE_API_URL` - Your Render backend URL + `/api`

## 🔑 Key Features

### Admin Dashboard (`/admin/*`)
- **Dashboard**: Overview with statistics and key metrics
- **Guests**: Manage all guest registrations
- **Tasks**: Wedding planning task management
- **Costs**: Budget tracking and cost management
- **Content**: Manage content shown to guests
- **Analytics**: Detailed analytics and reports

### Guest Portal (`/`)
- **Registration**: RSVP form with all guest information
- **Information**: Wedding details, venue info, schedule
- **Updates**: Guests can update their RSVP information

## 📊 Database Models

1. **User** - Admin users (groom, bride, planners)
2. **Guest** - Guest registrations and RSVPs
3. **Task** - Wedding planning tasks
4. **Cost** - Budget items and expenses
5. **Content** - Public content for guest portal

## 🔐 Authentication

- **Admin**: JWT-based authentication
- **Guests**: Public registration (no login required)
- **Protected Routes**: Admin routes require authentication

## 🛠️ Technology Stack

### Backend
- Flask (Python web framework)
- SQLAlchemy (ORM)
- Flask-JWT-Extended (Authentication)
- PostgreSQL (Production) / SQLite (Development)

### Frontend
- React 19
- Vite (Build tool)
- React Router (Routing)
- React Query (Server state)
- Tailwind CSS (Styling)
- Lucide React (Icons)

## 📝 API Endpoints

### Public Endpoints
- `POST /api/guests/register` - Guest registration
- `GET /api/content` - Get public content

### Admin Endpoints (Require JWT)
- `POST /api/auth/register` - Create admin user
- `POST /api/auth/login` - Admin login
- `GET /api/guests` - List all guests
- `GET /api/tasks` - List tasks
- `GET /api/costs` - List costs
- `GET /api/analytics/*` - Analytics endpoints
- `PUT /api/content/*` - Manage content

## 🎯 Next Steps

1. **Deploy Backend to Render**:
   - Create PostgreSQL database
   - Create web service
   - Configure environment variables
   - Deploy

2. **Deploy Frontend to Vercel**:
   - Connect GitHub repository
   - Configure build settings
   - Set environment variables
   - Deploy

3. **Post-Deployment**:
   - Create first admin user
   - Add initial content for guests
   - Test guest registration
   - Customize content

4. **Development**:
   - See [QUICK_START.md](./QUICK_START.md) for local development
   - See [BRAINSTORMING.md](./BRAINSTORMING.md) for feature ideas

## 📚 Documentation Files

- **README.md** - Main project documentation
- **QUICK_START.md** - Local development setup
- **DEPLOYMENT.md** - Detailed deployment guide
- **BRAINSTORMING.md** - Feature ideas and enhancements
- **SETUP_SUMMARY.md** - This file (overview)

## 🔄 Deployment Workflow

1. Push code to GitHub
2. Render automatically deploys backend
3. Vercel automatically deploys frontend
4. Update environment variables if needed
5. Test both deployments

## ⚠️ Important Notes

- **CORS**: Backend must have correct `FRONTEND_URL` for CORS
- **Database**: Use Render's internal database URL for production
- **Secrets**: Generate strong, random secrets for production
- **HTTPS**: Both platforms provide HTTPS by default
- **Environment**: Never commit `.env` files

## 🆘 Support

For issues:
1. Check deployment logs in Render/Vercel dashboards
2. Verify environment variables are set correctly
3. Check database connection
4. Review API endpoints in browser dev tools
5. See troubleshooting sections in DEPLOYMENT.md

