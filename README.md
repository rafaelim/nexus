# Nexus

A multi-domain home management application built with FastAPI (backend) and SolidJS (frontend). Track your finances, household expenses, groceries, and more.

## Features

- Transaction management (income/expenses)
- Category management
- Recurring expenses (ongoing and installment payments)
- Dashboard with charts and summaries
- Monthly expense tracking
- Simple user context (no authentication required for local use)

## Tech Stack

### Backend
- Python 3.11+
- FastAPI
- PostgreSQL
- SQLAlchemy Core (query builder)
- Alembic for migrations

### Frontend
- SolidJS
- TypeScript
- Tailwind CSS
- Chart.js
- Solid Router

## Development Setup

### Database (Docker)

1. Start the PostgreSQL container:
```bash
docker-compose up -d
```

This will start PostgreSQL on `localhost:5432` with:
- Database: `nexus`
- User: `postgres`
- Password: `postgres`

2. Verify the database is running:
```bash
docker-compose ps
```

To stop the database:
```bash
docker-compose down
```

To stop and remove volumes (⚠️ deletes all data):
```bash
docker-compose down -v
```

### Backend

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with the following content (configured for Docker):
```bash
# Database (Docker)
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/nexus

# Default User ID (matches the user created in seed.sql)
DEFAULT_USER_ID=00000000-0000-0000-0000-000000000001

# App
ENVIRONMENT=development
DEBUG=True
```

6. Initialize the database schema and seed default users:
```bash
# Option 1: Using the helper script (easiest)
cd backend
./scripts/init_db.sh

# Option 2: Using psql manually (password: postgres)
PGPASSWORD=postgres psql -h localhost -U postgres -d nexus -f db/schema.sql
PGPASSWORD=postgres psql -h localhost -U postgres -d nexus -f db/seed.sql

# Option 3: Using migrations
alembic upgrade head
PGPASSWORD=postgres psql -h localhost -U postgres -d nexus -f db/seed.sql
```

**Note:** You only need to run this step once when setting up the database, or after dropping/recreating it.

7. Start the API server (in a separate terminal):
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Frontend

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file (optional):
```
VITE_API_URL=http://localhost:8000
```

4. Start the development server (in a separate terminal):
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Running the Application

1. **Terminal 1** - Start the database:
   ```bash
   docker-compose up -d
   ```

2. **Terminal 2** - Start the backend API:
   ```bash
   cd backend
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   uvicorn app.main:app --reload
   ```

3. **Terminal 3** - Start the frontend:
   ```bash
   cd frontend
   npm run dev
   ```

Now you can access:
- Frontend: http://localhost:5173
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Project Structure

```
/
├── backend/
│   ├── app/
│   │   ├── api/v1/          # API endpoints
│   │   ├── core/             # Core utilities (config, database, security)
│   │   └── domain/           # Domain logic
│   │       └── finance/     # Finance domain
│   ├── db/
│   │   ├── migrations/       # Alembic migrations
│   │   └── schema.sql        # Database schema
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── pages/            # Page components
    │   │   └── finance/      # Finance pages
    │   ├── components/       # Generic components
    │   ├── services/         # API services
    │   └── shared/           # Shared utilities
    └── package.json
```

## API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for interactive API documentation.

## License

MIT

