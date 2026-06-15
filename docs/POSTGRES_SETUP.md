# PostgreSQL Setup

PostgreSQL is active on this machine and is accepting connections on `localhost:5432`.
pgAdmin 4 is also running.

The application needs a real database URL in `backend/.env`.

Example:

```env
DATABASE_URL=postgresql+psycopg://postgres:your_password@localhost:5432/enterprise_ai_copilot
```

Create the database from pgAdmin or psql:

```sql
CREATE DATABASE enterprise_ai_copilot;
```

Optional pgvector setup inside that database:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

Apply schema migrations after setting `DATABASE_URL`:

```bash
cd backend
python -m alembic upgrade head
```
