"""Build lambda.zip for AWS Lambda (Python 3.12, x86_64).

Run from anywhere:  python backend/build_lambda.py
Downloads Linux wheels, so it works on Windows/macOS too.
"""
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "build"
ZIP_BASE = ROOT / "lambda"  # make_archive adds .zip

shutil.rmtree(BUILD, ignore_errors=True)
(ROOT / "lambda.zip").unlink(missing_ok=True)

subprocess.check_call([
    sys.executable, "-m", "pip", "install",
    "-r", str(ROOT / "requirements.txt"),
    "--target", str(BUILD),
    "--platform", "manylinux2014_x86_64",
    "--implementation", "cp",
    "--python-version", "3.12",
    "--only-binary=:all:",
    "--upgrade",
])

shutil.copytree(ROOT / "app", BUILD / "app", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))

# shutil writes forward-slash entry names; PowerShell 5.1 Compress-Archive does not, which breaks Lambda imports
shutil.make_archive(str(ZIP_BASE), "zip", BUILD)
print(f"Built {ZIP_BASE}.zip  ->  handler: app.main.handler")
