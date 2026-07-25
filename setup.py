#!/usr/bin/env python3
"""Bootstrap the development environment for the application orchestration platform."""

from __future__ import annotations

import argparse
import logging
import os
import shutil
import subprocess
import sys
import venv
from pathlib import Path
from typing import List, Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parent
BACKEND_DIR = REPO_ROOT / "backend" / "fastapi"
FRONTEND_DIR = REPO_ROOT / "frontend"
VENV_DIR = REPO_ROOT / ".venv"

def run_command(command: List[str], cwd: Optional[Path] = None, env: Optional[dict] = None) -> None:
    logger.info(f"> {' '.join(command)}")
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
        logger.info(f"Creating Python virtual environment at {VENV_DIR}")
        builder = venv.EnvBuilder(with_pip=True, clear=False, symlinks=False)
        builder.create(VENV_DIR)

    python_executable = python_executable_for_env(VENV_DIR)
    if not python_executable.exists():
        raise RuntimeError(f"Python virtual environment was not created successfully: {python_executable}")

    return python_executable

def install_backend_requirements(python_executable: Path) -> None:
    logger.info("Installing backend dependencies...")
    run_command([str(python_executable), "-m", "pip", "install", "--upgrade", "pip"])
    run_command([str(python_executable), "-m", "pip", "install", "-r", str(BACKEND_DIR / "requirements.txt")])

def clean_frontend_lockfiles() -> None:
    logger.info("Cleaning frontend node_modules and package-lock.json to avoid peer dependency conflicts...")
    paths_to_remove = [
        FRONTEND_DIR / "node_modules",
        FRONTEND_DIR / "package-lock.json"
    ]
    for p in paths_to_remove:
        if p.exists():
            if p.is_dir():
                shutil.rmtree(p, ignore_errors=True)
            else:
                p.unlink(missing_ok=True)

def install_frontend_dependencies(npm_executable: str) -> None:
    clean_frontend_lockfiles()
    logger.info("Installing frontend dependencies...")
    run_command([npm_executable, "install", "--prefix", str(FRONTEND_DIR), "--no-audit", "--no-fund"], cwd=REPO_ROOT)

def create_cli_wrappers() -> None:
    logger.info("Creating platform CLI wrappers...")
    bat_path = REPO_ROOT / "platform.bat"
    sh_path = REPO_ROOT / "platform"

    with bat_path.open("w", encoding="utf-8") as f:
        f.write("@echo off\n")
        f.write('python "%~dp0platform.py" %*\n')

    with sh_path.open("w", encoding="utf-8") as f:
        f.write("#!/usr/bin/env bash\n")
        f.write('python3 "$(dirname "$0")/platform.py" "$@"\n')

    if os.name != "nt":
        os.chmod(sh_path, 0o755)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bootstrap the platform for local development")
    parser.add_argument("--check-only", action="store_true", help="Validate prerequisites without starting services")
    return parser.parse_args()

def main() -> int:
    args = parse_args()

    logger.info(f"Repository root: {REPO_ROOT}")

    python_cmd = ensure_command("python")
    npm_cmd = ensure_command("npm")

    if args.check_only:
        logger.info("Check-only mode enabled. Prerequisites look good.")
        return 0

    logger.info("Creating or reusing the project virtual environment...")
    python_executable = create_virtual_environment()
    if not python_executable.exists():
        raise RuntimeError("Python virtual environment was not created successfully")

    install_backend_requirements(python_executable)
    install_frontend_dependencies(npm_cmd)

    create_cli_wrappers()

    logger.info("Setup complete! You can now use the `platform` CLI.")
    logger.info("  Run 'platform start' to launch the application.")
    logger.info("  Run 'platform stop' to stop running services.")
    logger.info("  Run 'platform uninstall' to clean up dependencies.")
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise SystemExit(130)
    except RuntimeError as exc:
        logger.error(f"ERROR: {exc}")
        raise SystemExit(1)
