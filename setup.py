#!/usr/bin/env python3
"""Bootstrap the development environment for the application orchestration platform."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import venv
from pathlib import Path
from typing import Any, Dict, List, Optional


REPO_ROOT = Path(__file__).resolve().parent
BACKEND_DIR = REPO_ROOT / "backend" / "fastapi"
FRONTEND_DIR = REPO_ROOT / "frontend"
LOGS_DIR = REPO_ROOT / "logs"
VENV_DIR = REPO_ROOT / ".venv"
ASSETS_DIR = REPO_ROOT / "assets"
SERVICE_MANIFEST_PATH = ASSETS_DIR / "service-manifest.json"
SERVICE_LOG_DIR = LOGS_DIR / "services"


def run_command(command: List[str], cwd: Optional[Path] = None, env: Optional[dict] = None) -> None:
    print(f"> {' '.join(command)}")
    completed = subprocess.run(command, cwd=str(cwd) if cwd else None, env=env, check=False)
    if completed.returncode != 0:
        raise RuntimeError(f"Command failed with exit code {completed.returncode}: {' '.join(command)}")


def ensure_command(name: str) -> str:
    candidates = [name]
    if os.name == "nt":
        if name == "python":
            candidates = ["py", "python", "python.exe", "python3"]
        elif name == "npm":
            candidates = ["npm.cmd", "npm", "npx.cmd", "npx"]
        elif name == "docker":
            candidates = ["docker.exe", "docker"]

    for candidate in candidates:
        resolved = shutil.which(candidate)
        if resolved:
            return resolved

    raise RuntimeError(f"Required command not found on PATH: {name}")


def python_executable_for_env(env_dir: Path) -> Path:
    if os.name == "nt":
        return env_dir / "Scripts" / "python.exe"
    return env_dir / "bin" / "python"


def create_virtual_environment() -> Path:
    if VENV_DIR.exists() and not VENV_DIR.is_dir():
        raise RuntimeError(f"Expected {VENV_DIR} to be a directory, but found a file")

    if not VENV_DIR.exists():
        print(f"Creating Python virtual environment at {VENV_DIR}")
        builder = venv.EnvBuilder(with_pip=True, clear=False, symlinks=False)
        builder.create(VENV_DIR)

    python_executable = python_executable_for_env(VENV_DIR)
    if not python_executable.exists():
        raise RuntimeError(f"Python virtual environment was not created successfully: {python_executable}")

    return python_executable


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
    creationflags = 0
    if os.name == "nt":
        creationflags = subprocess.CREATE_NEW_CONSOLE
    return subprocess.Popen(
        [str(python_executable), "-m", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
        cwd=str(BACKEND_DIR),
        stdout=backend_log.open("a", encoding="utf-8"),
        stderr=subprocess.STDOUT,
        text=True,
        creationflags=creationflags,
    )


def start_frontend(npm_executable: str) -> subprocess.Popen:
    frontend_log = LOGS_DIR / "frontend.log"
    print("Starting Angular frontend...")
    creationflags = 0
    if os.name == "nt":
        creationflags = subprocess.CREATE_NEW_CONSOLE
    return subprocess.Popen(
        [npm_executable, "start"],
        cwd=str(FRONTEND_DIR),
        stdout=frontend_log.open("a", encoding="utf-8"),
        stderr=subprocess.STDOUT,
        text=True,
        creationflags=creationflags,
    )


def ensure_logs_dir() -> None:
    LOGS_DIR.mkdir(exist_ok=True)
    SERVICE_LOG_DIR.mkdir(exist_ok=True)


def ensure_assets_layout() -> None:
    ASSETS_DIR.mkdir(exist_ok=True)
    (ASSETS_DIR / "postgres").mkdir(exist_ok=True)
    (ASSETS_DIR / "keycloak").mkdir(exist_ok=True)
    (ASSETS_DIR / "oauth2-proxy").mkdir(exist_ok=True)


def load_service_manifest() -> Dict[str, Any]:
    if not SERVICE_MANIFEST_PATH.exists():
        default_manifest = {
            "postgres": {
                "path": "assets/postgres/postgres.exe",
                "args": ["-D", "assets/postgres/data"],
                "cwd": "assets/postgres",
            },
            "keycloak": {
                "path": "assets/keycloak/kc.bat",
                "args": [],
                "cwd": "assets/keycloak",
            },
            "oauth2-proxy": {
                "path": "assets/oauth2-proxy/oauth2-proxy.exe",
                "args": [],
                "cwd": "assets/oauth2-proxy",
            },
        }
        with SERVICE_MANIFEST_PATH.open("w", encoding="utf-8") as handle:
            json.dump(default_manifest, handle, indent=2)
        return default_manifest

    with SERVICE_MANIFEST_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def start_asset_services() -> List[subprocess.Popen]:
    ensure_assets_layout()
    manifest = load_service_manifest()
    processes: List[subprocess.Popen] = []

    if not manifest:
        print("No service entries were found in the asset manifest.")
        return processes

    for name, config in manifest.items():
        asset_path = config.get("path", "")
        if not asset_path:
            print(f"Skipping {name}: no executable path configured")
            continue

        resolved_path = REPO_ROOT / asset_path if not Path(asset_path).is_absolute() else Path(asset_path)
        if not resolved_path.exists():
            print(f"Skipping {name}: expected executable not found at {resolved_path}")
            continue

        args = list(config.get("args", []))
        cwd = REPO_ROOT / config.get("cwd", "assets") if not Path(config.get("cwd", "assets")).is_absolute() else Path(config.get("cwd", "assets"))

        if resolved_path.suffix.lower() in {".bat", ".cmd"}:
            command = ["cmd.exe", "/c", str(resolved_path)]
        elif resolved_path.suffix.lower() == ".ps1":
            command = ["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", str(resolved_path)]
        else:
            command = [str(resolved_path)]

        log_path = SERVICE_LOG_DIR / f"{name}.log"
        print(f"Starting asset service '{name}' from {resolved_path}")
        creationflags = subprocess.CREATE_NEW_CONSOLE if os.name == "nt" else 0
        handle = log_path.open("a", encoding="utf-8")
        processes.append(
            subprocess.Popen(
                command + args,
                cwd=str(cwd),
                stdout=handle,
                stderr=subprocess.STDOUT,
                text=True,
                creationflags=creationflags,
            )
        )

    return processes


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bootstrap the platform for local development")
    parser.add_argument("--check-only", action="store_true", help="Validate prerequisites without starting services")
    parser.add_argument("--skip-start", action="store_true", help="Prepare dependencies and infrastructure without launching the backend/frontend")
    parser.add_argument("--use-docker", action="store_true", help="Use Docker Compose instead of the Windows process-based startup flow")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    print(f"Repository root: {REPO_ROOT}")
    ensure_logs_dir()

    python_cmd = ensure_command("python")
    npm_cmd = ensure_command("npm")

    if args.check_only:
        print("Check-only mode enabled. Prerequisites look good.")
        return 0

    print("Creating or reusing the project virtual environment...")
    python_executable = create_virtual_environment()
    if not python_executable.exists():
        raise RuntimeError("Python virtual environment was not created successfully")

    if os.name == "nt":
        print("Windows mode detected. Using a process-based startup flow and skipping Docker Compose by default.")
        print("Install the required local dependencies on this machine first, then start the platform processes directly.")
        start_asset_services()
    elif args.use_docker:
        docker = ensure_command("docker")
        start_docker_services()
    else:
        print("Non-Windows host detected. Docker Compose is not started automatically; use --use-docker to enable it.")

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
