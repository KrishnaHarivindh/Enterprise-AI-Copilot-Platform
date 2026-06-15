# Enterprise AI Copilot Platform Plan

## Goal

Build a flagship final-year CSE project that demonstrates practical industry skills across AI, NLP, full stack development, databases, cloud readiness, DevOps, and security.

## Milestone 1: Platform Foundation

Deliverables:

- Backend API with FastAPI
- Frontend dashboard shell with React and TypeScript
- PostgreSQL service with pgvector extension
- Environment configuration
- Health-check API
- Initial project documentation

Acceptance criteria:

- Backend app imports successfully
- `/api/v1/health` returns a valid response
- Frontend builds successfully
- Docker Compose can start PostgreSQL
- Folder structure supports future auth, RAG, and agent modules

## Milestone 2: Authentication and Users

Deliverables:

- User model
- Password hashing
- JWT login
- Role-based access control
- Protected frontend routes

Acceptance criteria:

- Users can register with validated email and strong password rules
- First registered user becomes `ADMIN`
- Login returns access and refresh tokens
- `/api/v1/auth/me` requires a bearer token
- `/api/v1/users` is restricted to admins

## Milestone 3: Document Intelligence

Deliverables:

- Upload documents
- Extract text from PDF, DOCX, TXT, and CSV
- Store document metadata
- Chunk documents for retrieval
- Alembic database migrations
- Document versioning

## Milestone 4: RAG Chat

Deliverables:

- Embedding generation
- Vector search using pgvector
- Chat API
- Source citations
- Conversation history

Current foundation:

- `document_chunks` table
- chunking service
- sentence-transformers embedding service
- pgvector semantic search
- basic grounded chat response with sources

## Milestone 5: Multi-Agent Workflows

Deliverables:

- Summarizer agent
- Report generator agent
- Data analyst agent
- Meeting notes agent
- Workflow run tracking

## Milestone 6: Production Hardening

Deliverables:

- Structured logging
- API tests
- Frontend tests
- Rate limiting
- Audit logs
- CI pipeline
- Deployment guide
