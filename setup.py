#!/usr/bin/env python3
"""Bootstrap the development environment for the application orchestration platform."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import venv
from pathlib import Path
from typing import List, Optional


REPO_ROOT = Path(__file__).resolve().parent
BACKEND_DIR = REPO_ROOT / "backend" / "fastapi"
FRONTEND_DIR = REPO_ROOT / "frontend"
LOGS_DIR = REPO_ROOT / "logs"
VENV_DIR = REPO_ROOT / ".venv"


def run_command(command: List[str], cwd: Optional[Path] = None, env: Optional[dict] = None) -> None:
    print(f"> {' '.join(command)}")
    completed = subprocess.run(command, cwd=str(cwd) if cwd else None, env=env, check=False)
    if completed.returncode != 0:
        raise RuntimeError(f"Command failed with exit code {completed.returncode}: {' '.join(command)}")


def ensure_command(name: str) -> str:
    resolved = shutil.which(name)
    if resolved:
        return resolved
    if os.name == "nt" and name == "npm":
        resolved = shutil.which("npm.cmd")
        if resolved:
            return resolved
    raise RuntimeError(f"Required command not found on PATH: {name}")


def create_virtual_environment() -> Path:
    if VENV_DIR.exists():
        return VENV_DIR

    print(f"Creating Python virtual environment at {VENV_DIR}")
    builder = venv.EnvBuilder(with_pip=True, clear=False, symlinks=False)
    builder.create(VENV_DIR)

    if os.name == "nt":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def install_backend_requirements(python_executable: Path) -> None:
    print("Installing backend dependencies...")
    run_command([str(python_executable), "-m", "pip", "install", "--upgrade", "pip"])
    run_command([str(python_executable), "-m", "pip", "install", "-r", str(BACKEND_DIR / "requirements.txt")])


def install_frontend_dependencies(npm_executable: str) -> None:
    print("Installing frontend dependencies...")
    run_command([npm_executable, "install", "--prefix", str(FRONTEND_DIR), "--no-audit", "--no-fund"], cwd=REPO_ROOT)


def start_docker_services() -> None:
    print("Starting shared infrastructure services with Docker Compose...")
    run_command(["docker", "compose", "up", "-d", "postgres", "keycloak", "openfga", "oauth2-proxy"], cwd=REPO_ROOT)


def start_backend(python_executable: Path) -> subprocess.Popen:
    backend_log = LOGS_DIR / "backend.log"
    print("Starting FastAPI backend...")
    return subprocess.Popen(
        [str(python_executable), "-m", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
        cwd=str(BACKEND_DIR),
        stdout=backend_log.open("a", encoding="utf-8"),
        stderr=subprocess.STDOUT,
        text=True,
    )


def start_frontend(npm_executable: str) -> subprocess.Popen:
    frontend_log = LOGS_DIR / "frontend.log"
    print("Starting Angular frontend...")
    return subprocess.Popen(
        [npm_executable, "start"],
        cwd=str(FRONTEND_DIR),
        stdout=frontend_log.open("a", encoding="utf-8"),
        stderr=subprocess.STDOUT,
        text=True,
    )


def ensure_logs_dir() -> None:
    LOGS_DIR.mkdir(exist_ok=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bootstrap the platform for local development")
    parser.add_argument("--check-only", action="store_true", help="Validate prerequisites without starting services")
    parser.add_argument("--skip-start", action="store_true", help="Prepare dependencies and infrastructure without launching the backend/frontend")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    print(f"Repository root: {REPO_ROOT}")
    ensure_logs_dir()

    docker = ensure_command("docker")
    python_cmd = ensure_command("python")
    npm_cmd = ensure_command("npm")

    if args.check_only:
        print("Check-only mode enabled. Prerequisites look good.")
        return 0

    print("Creating or reusing the project virtual environment...")
    python_executable = create_virtual_environment()
    if not python_executable.exists():
        raise RuntimeError("Python virtual environment was not created successfully")

    start_docker_services()
    install_backend_requirements(python_executable)
    install_frontend_dependencies(npm_cmd)

    if args.skip_start:
        print("Dependency installation complete. Skipping backend/frontend launch.")
        return 0

    backend_process = start_backend(python_executable)
    frontend_process = start_frontend(npm_cmd)

    print("Development stack started.")
    print("- Frontend: http://localhost:4200")
    print("- FastAPI docs: http://localhost:8000/docs")
    print("- Keycloak: http://localhost:8080")
    print("- OAuth2 Proxy: http://localhost:4180")
    print(f"- Backend log: {LOGS_DIR / 'backend.log'}")
    print(f"- Frontend log: {LOGS_DIR / 'frontend.log'}")
    print(f"- Backend process id: {backend_process.pid}")
    print(f"- Frontend process id: {frontend_process.pid}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise SystemExit(130)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
