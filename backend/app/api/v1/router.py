from fastapi import APIRouter

from app.api.v1.routes import admin, agents, audit_logs, auth, chat, documents, health, search, users

api_router = APIRouter()
api_router.include_router(admin.router, tags=["admin"])
api_router.include_router(agents.router, tags=["agents"])
api_router.include_router(audit_logs.router, tags=["audit logs"])
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(chat.router, tags=["chat"])
api_router.include_router(documents.router, tags=["documents"])
api_router.include_router(health.router, tags=["health"])
api_router.include_router(search.router, tags=["search"])
api_router.include_router(users.router, tags=["users"])
