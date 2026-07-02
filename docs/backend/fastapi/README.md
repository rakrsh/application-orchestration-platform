# Backend Service

The backend service is a FastAPI application that exposes health and application-management endpoints.

## Current capabilities

- Health check endpoint
- Application listing endpoint
- Application creation endpoint with basic role checks
- Database-backed storage for applications

## Runtime notes

The service is containerized through Docker Compose and connects to the shared PostgreSQL database defined in the repository stack.
