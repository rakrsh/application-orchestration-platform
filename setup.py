#!/usr/bin/env python3
"""Bootstrap the development environment for the application orchestration platform."""

from __future__ import annotations

import argparse
import logging
import os
import re
import shutil
import subprocess
import urllib.request
import venv
import zipfile
from pathlib import Path
from typing import List, Optional

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parent
BACKEND_DIR = REPO_ROOT / "backend" / "fastapi"
FRONTEND_DIR = REPO_ROOT / "frontend"
VENV_DIR = REPO_ROOT / ".venv"
NGINX_DIR = REPO_ROOT / "tools" / "nginx"
NGINX_ZIP_PATH = NGINX_DIR / "nginx.zip"


def run_command(
    command: List[str], cwd: Optional[Path] = None, env: Optional[dict] = None
) -> None:
    logger.info(f"> {' '.join(command)}")
    completed = subprocess.run(
        command, cwd=str(cwd) if cwd else None, env=env, check=False
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"Command failed with exit code {completed.returncode}: {' '.join(command)}"
        )


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
        raise RuntimeError(
            f"Python virtual environment was not created successfully: {python_executable}"
        )

    return python_executable


def install_backend_requirements(python_executable: Path) -> None:
    logger.info("Installing backend dependencies...")
    run_command([str(python_executable), "-m", "pip", "install", "--upgrade", "pip"])
    run_command(
        [
            str(python_executable),
            "-m",
            "pip",
            "install",
            "-r",
            str(BACKEND_DIR / "requirements.txt"),
        ]
    )


def clean_frontend_lockfiles() -> None:
    logger.info(
        "Cleaning frontend node_modules and package-lock.json to avoid peer dependency conflicts..."
    )
    paths_to_remove = [
        FRONTEND_DIR / "node_modules",
        FRONTEND_DIR / "package-lock.json",
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
    run_command(
        [
            npm_executable,
            "install",
            "--prefix",
            str(FRONTEND_DIR),
            "--no-audit",
            "--no-fund",
        ],
        cwd=REPO_ROOT,
    )


def build_frontend_production(npm_executable: str) -> None:
    logger.info("Building the Angular frontend for production...")
    run_command([npm_executable, "run", "build"], cwd=FRONTEND_DIR)


def build_nginx_download_url(version: str) -> str:
    return f"https://nginx.org/download/nginx-{version}.zip"


def extract_latest_nginx_version(download_page: str) -> str:
    matches = re.findall(r"nginx-(\d+\.\d+\.\d+)\.zip", download_page)
    if not matches:
        raise RuntimeError(
            "Could not determine the latest nginx release from nginx.org"
        )
    return sorted(
        matches, key=lambda value: tuple(int(part) for part in value.split("."))
    )[-1]


def install_nginx_windows() -> None:
    if os.name != "nt":
        return

    logger.info("Preparing nginx for Windows local installation...")
    NGINX_DIR.mkdir(parents=True, exist_ok=True)

    try:
        with urllib.request.urlopen("https://nginx.org/download/") as response:
            html = response.read().decode("utf-8", errors="replace")
    except Exception as exc:  # pragma: no cover - network dependency
        raise RuntimeError(
            f"Unable to query nginx.org for the latest release: {exc}"
        ) from exc

    version = extract_latest_nginx_version(html)
    download_url = build_nginx_download_url(version)
    archive_path = NGINX_ZIP_PATH

    logger.info(f"Downloading nginx {version} from {download_url}")
    with urllib.request.urlopen(download_url) as response, archive_path.open(
        "wb"
    ) as handle:
        shutil.copyfileobj(response, handle)

    logger.info("Extracting nginx archive...")
    with zipfile.ZipFile(archive_path) as archive:
        archive.extractall(NGINX_DIR)

    extracted_root = next(
        (
            path
            for path in NGINX_DIR.iterdir()
            if path.is_dir() and path.name.startswith("nginx-")
        ),
        None,
    )
    if extracted_root is None:
        raise RuntimeError(
            "nginx archive did not contain an expected extracted directory"
        )

    nginx_exe = extracted_root / "nginx.exe"
    if not nginx_exe.exists():
        raise RuntimeError(f"nginx executable was not found at {nginx_exe}")

    logger.info(f"nginx installed to {extracted_root}")


def configure_frontend_nginx() -> None:
    if os.name != "nt":
        return

    nginx_root = next(
        (
            path
            for path in NGINX_DIR.iterdir()
            if path.is_dir() and path.name.startswith("nginx-")
        ),
        None,
    )
    if nginx_root is None:
        raise RuntimeError("nginx installation was not found; run setup.py again")

    conf_path = nginx_root / "conf" / "nginx.conf"
    if not conf_path.exists():
        raise RuntimeError(f"nginx configuration file was not found at {conf_path}")

    frontend_conf_template = FRONTEND_DIR / "nginx" / "default.conf"
    if not frontend_conf_template.exists():
        raise RuntimeError(
            f"Frontend nginx config was not found at {frontend_conf_template}"
        )

    conf_contents = conf_path.read_text(encoding="utf-8")
    if "include conf.d/*.conf;" not in conf_contents:
        conf_contents = conf_contents.replace(
            "http {", "http {\n    include conf.d/*.conf;\n"
        )
        conf_path.write_text(conf_contents, encoding="utf-8")

    conf_dir = nginx_root / "conf" / "conf.d"
    conf_dir.mkdir(parents=True, exist_ok=True)

    frontend_root = FRONTEND_DIR / "dist" / "temp-app" / "browser"
    frontend_conf = frontend_conf_template.read_text(encoding="utf-8")
    frontend_conf = frontend_conf.replace("__PORT__", "4200")
    frontend_conf = frontend_conf.replace(
        "__FRONTEND_ROOT__", str(frontend_root).replace("\\", "/")
    )
    (conf_dir / "default.conf").write_text(frontend_conf, encoding="utf-8")

    logger.info(f"Configured nginx to serve the Angular frontend from {frontend_root}")


def start_frontend_nginx_windows() -> None:
    if os.name != "nt":
        return

    nginx_root = next(
        (
            path
            for path in NGINX_DIR.iterdir()
            if path.is_dir() and path.name.startswith("nginx-")
        ),
        None,
    )
    if nginx_root is None:
        raise RuntimeError("nginx installation was not found; run setup.py again")

    nginx_exe = nginx_root / "nginx.exe"
    if not nginx_exe.exists():
        raise RuntimeError(f"nginx executable was not found at {nginx_exe}")

    config_path = nginx_root / "conf" / "nginx.conf"
    if not config_path.exists():
        raise RuntimeError(f"nginx configuration file was not found at {config_path}")

    logger.info("Starting nginx to serve the Angular UI on http://localhost:4200")
    subprocess.Popen(
        [str(nginx_exe), "-c", str(config_path)],
        cwd=str(nginx_root),
        creationflags=subprocess.CREATE_NEW_CONSOLE,
    )


def create_cli_wrappers() -> None:
    logger.info("Creating platform CLI wrappers...")
    bat_path = REPO_ROOT / "platform.bat"
    sh_path = REPO_ROOT / "platform"

    with bat_path.open("w", encoding="utf-8") as f:
        f.write("@echo off\n")
        f.write('python "%~dp0cli.py" %*\n')

    with sh_path.open("w", encoding="utf-8") as f:
        f.write("#!/usr/bin/env bash\n")
        f.write('python3 "$(dirname "$0")/cli.py" "$@"\n')

    if os.name != "nt":
        os.chmod(sh_path, 0o755)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Bootstrap the platform for local development"
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Validate prerequisites without starting services",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    logger.info(f"Repository root: {REPO_ROOT}")

    ensure_command("python")
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
    build_frontend_production(npm_cmd)
    install_nginx_windows()
    configure_frontend_nginx()
    start_frontend_nginx_windows()

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
