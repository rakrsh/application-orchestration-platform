#!/usr/bin/env python3
"""Platform CLI for managing the application orchestration platform services."""

import argparse
import json
import logging
import os
import shutil
import subprocess
import sys
import webbrowser
import time
import signal
from pathlib import Path
from typing import Any, Dict, List, Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("platform_cli")

REPO_ROOT = Path(__file__).resolve().parent
BACKEND_DIR = REPO_ROOT / "backend" / "fastapi"
FRONTEND_DIR = REPO_ROOT / "frontend"
LOGS_DIR = REPO_ROOT / "logs"
VENV_DIR = REPO_ROOT / ".venv"
ASSETS_DIR = REPO_ROOT / "assets"
SERVICE_MANIFEST_PATH = ASSETS_DIR / "service-manifest.json"
SERVICE_LOG_DIR = LOGS_DIR / "services"
STATE_FILE = REPO_ROOT / ".platform_state.json"

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

def run_command(command: List[str], cwd: Optional[Path] = None, env: Optional[dict] = None) -> None:
    logger.info(f"> {' '.join(command)}")
    completed = subprocess.run(command, cwd=str(cwd) if cwd else None, env=env, check=False)
    if completed.returncode != 0:
        raise RuntimeError(f"Command failed with exit code {completed.returncode}: {' '.join(command)}")

def load_service_manifest() -> Dict[str, Any]:
    if not SERVICE_MANIFEST_PATH.exists():
        return {}
    with SERVICE_MANIFEST_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)

def ensure_logs_dir() -> None:
    LOGS_DIR.mkdir(exist_ok=True)
    SERVICE_LOG_DIR.mkdir(exist_ok=True)

def start_asset_services() -> List[int]:
    ensure_logs_dir()
    manifest = load_service_manifest()
    pids: List[int] = []

    if not manifest:
        return pids

    for name, config in manifest.items():
        asset_path = config.get("path", "")
        if not asset_path:
            continue

        resolved_path = REPO_ROOT / asset_path if not Path(asset_path).is_absolute() else Path(asset_path)
        if not resolved_path.exists():
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
        logger.info(f"Starting asset service '{name}'...")
        creationflags = subprocess.CREATE_NEW_CONSOLE if os.name == "nt" else 0
        handle = log_path.open("a", encoding="utf-8")
        proc = subprocess.Popen(
            command + args,
            cwd=str(cwd),
            stdout=handle,
            stderr=subprocess.STDOUT,
            text=True,
            creationflags=creationflags,
        )
        pids.append(proc.pid)

    return pids

def start_backend(python_executable: Path) -> int:
    backend_log = LOGS_DIR / "backend.log"
    logger.info("Starting FastAPI backend...")
    creationflags = subprocess.CREATE_NEW_CONSOLE if os.name == "nt" else 0
    proc = subprocess.Popen(
        [str(python_executable), "-m", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
        cwd=str(BACKEND_DIR),
        stdout=backend_log.open("a", encoding="utf-8"),
        stderr=subprocess.STDOUT,
        text=True,
        creationflags=creationflags,
    )
    return proc.pid

def start_frontend(npm_executable: str) -> int:
    frontend_log = LOGS_DIR / "frontend.log"
    logger.info("Starting Angular frontend...")
    creationflags = subprocess.CREATE_NEW_CONSOLE if os.name == "nt" else 0
    proc = subprocess.Popen(
        [npm_executable, "start"],
        cwd=str(FRONTEND_DIR),
        stdout=frontend_log.open("a", encoding="utf-8"),
        stderr=subprocess.STDOUT,
        text=True,
        creationflags=creationflags,
    )
    return proc.pid

def cmd_start(args: argparse.Namespace) -> None:
    if STATE_FILE.exists():
        logger.warning("Platform is already running (state file exists). Use 'platform stop' first.")
        sys.exit(1)

    logger.info("Starting platform services...")
    ensure_logs_dir()

    python_executable = python_executable_for_env(VENV_DIR)
    if not python_executable.exists():
        logger.error("Virtual environment not found. Please run 'python setup.py' first.")
        sys.exit(1)

    npm_cmd = ensure_command("npm")
    pids = []

    if os.name == "nt":
        pids.extend(start_asset_services())
    else:
        logger.info("Non-Windows host. Assuming Docker is managing assets.")

    pids.append(start_backend(python_executable))
    pids.append(start_frontend(npm_cmd))

    logger.info(f"Saving {len(pids)} process IDs to state file...")
    with STATE_FILE.open("w", encoding="utf-8") as f:
        json.dump({"pids": pids}, f)

    logger.info("Platform services launched.")
    logger.info("Waiting for frontend to be available...")
    time.sleep(5)
    logger.info("Opening UI in browser: http://localhost:4200")
    webbrowser.open("http://localhost:4200")

def cmd_stop(args: argparse.Namespace) -> None:
    if not STATE_FILE.exists():
        logger.info("Platform does not appear to be running (no state file found).")
        return

    with STATE_FILE.open("r", encoding="utf-8") as f:
        state = json.load(f)

    pids = state.get("pids", [])
    logger.info(f"Stopping {len(pids)} processes...")

    for pid in pids:
        try:
            if os.name == "nt":
                subprocess.run(["taskkill", "/F", "/T", "/PID", str(pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                os.kill(pid, signal.SIGTERM)
        except Exception as e:
            logger.error(f"Failed to kill process {pid}: {e}")

    STATE_FILE.unlink()
    logger.info("Platform stopped.")

def cmd_uninstall(args: argparse.Namespace) -> None:
    logger.info("Uninstalling platform dependencies...")
    cmd_stop(args)

    paths_to_remove = [
        VENV_DIR,
        LOGS_DIR,
        FRONTEND_DIR / "node_modules",
        FRONTEND_DIR / ".angular",
        FRONTEND_DIR / "package-lock.json"
    ]

    for path in paths_to_remove:
        if path.exists():
            logger.info(f"Removing {path}...")
            if path.is_dir():
                shutil.rmtree(path, ignore_errors=True)
            else:
                path.unlink(missing_ok=True)

    logger.info("Uninstall complete.")

def main() -> int:
    parser = argparse.ArgumentParser(description="Application Orchestration Platform CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("start", help="Start the platform services and launch the UI")
    subparsers.add_parser("stop", help="Stop the running platform services")
    subparsers.add_parser("uninstall", help="Stop services and remove installed dependencies")

    args = parser.parse_args()

    if args.command == "start":
        cmd_start(args)
    elif args.command == "stop":
        cmd_stop(args)
    elif args.command == "uninstall":
        cmd_uninstall(args)

    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception as e:
        logger.error(f"ERROR: {e}")
        sys.exit(1)
