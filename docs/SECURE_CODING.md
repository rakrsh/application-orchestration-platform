# Secure Coding Guidelines

## 1. General Principles
- **Least Privilege:** Always run applications with the minimum necessary permissions (e.g., non-root Docker users).
- **Defense in Depth:** Apply multiple layers of security controls.
- **Fail Securely:** Applications should fail in a secure state and not leak stack traces or sensitive data.

## 2. Python / FastAPI (Backend)
- **Input Validation:** Use Pydantic models for all incoming request bodies and query parameters.
- **SQL Injection Prevention:** Use SQLAlchemy ORM or parameterized queries. Never use string concatenation for SQL.
- **Dependency Management:** Pin dependencies in `requirements.txt` / `requirements.lock`. Regularly run `pip-audit`.
- **Error Handling:** Return generic HTTP error messages (e.g., 400 Bad Request) rather than raw exceptions.

## 3. TypeScript / Angular (Frontend)
- **XSS Prevention:** Rely on Angular's built-in DomSanitizer. Avoid `[innerHTML]` unless explicitly sanitizing.
- **CSP (Content Security Policy):** Ensure the frontend is served with strict CSP headers.
- **Dependency Management:** Run `npm audit` frequently and use `package-lock.json`.

## 4. Code Review Checklist
- Does the code introduce any new dependencies? (If so, have they been vetted?)
- Are all new inputs validated?
- Are errors handled securely without leaking sensitive info?
- Are tests provided for the new logic, including negative test cases?
