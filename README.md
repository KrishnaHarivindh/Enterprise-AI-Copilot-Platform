# Enterprise AI Copilot Platform

Production-style AI copilot foundation for document intelligence, RAG chat, multi-agent workflows, analytics, and enterprise deployment.

## Overview

Enterprise AI Copilot Platform is a full-stack AI application designed to demonstrate how modern organizations can combine authentication, document intelligence, vector search, chat workflows, and admin analytics into one secure internal platform.

The project focuses on clean architecture, role-based access control, API-first development, and an extensible backend structure for RAG and agentic workflows.

## Key Features

- FastAPI backend with versioned API routes
- React and TypeScript frontend workspace
- User registration and login
- JWT access and refresh token flow
- bcrypt password hashing
- Role-based access control
- Protected frontend workspace
- PostgreSQL and pgvector-ready Docker Compose setup
- Document chunking and embedding pipeline foundation
- Semantic search endpoint
- RAG chat endpoint foundation
- Multi-agent workflow endpoints for summaries, reports, and meeting notes
- Conversation history APIs
- Admin metrics endpoint

## Tech Stack

**Backend:** Python, FastAPI, SQLAlchemy, Alembic  
**Frontend:** React, TypeScript, Vite  
**Database:** PostgreSQL, pgvector-ready architecture  
**AI:** RAG, embeddings, semantic search, multi-agent workflows  
**Security:** JWT, bcrypt, RBAC  
**DevOps:** Docker Compose

## Project Structure

```text
Enterprise-AI-Copilot-Platform/
  backend/
    app/
      api/v1/           Versioned API routes
      agents/           Agent workflow modules
      core/             Configuration and security
      db/               Database setup
      models/           SQLAlchemy models
      rag/              Retrieval and embedding logic
      schemas/          Pydantic schemas
      services/         Business logic
    tests/
  frontend/
    src/
      components/
      pages/
      services/
      types/
  docs/
```

## Quick Start

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend:

```text
http://localhost:8000
```

### Database

```bash
docker compose up -d postgres
cd backend
python -m alembic upgrade head
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

## API Highlights

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
- `GET /api/v1/users`
- `POST /api/v1/search`
- `POST /api/v1/chat`
- `POST /api/v1/agents/summarize`
- `POST /api/v1/agents/report`
- `POST /api/v1/agents/meeting-notes`
- `GET /api/v1/admin/metrics`

## Roadmap

1. Platform foundation
2. Authentication and role-based authorization
3. Document upload and text extraction
4. Embedding pipeline with pgvector
5. RAG chatbot with source citations
6. Multi-agent workflows
7. Admin analytics dashboard
8. Testing, observability, and deployment hardening

## Portfolio Note

This project demonstrates enterprise application architecture, secure authentication, AI workflow design, RAG foundations, and full-stack implementation using modern engineering practices.
