"""Prepare pinned Direct Mode SDK cache from genvm-lint's official download.

No network calls, no contract deployment, no wallet material.
"""
from pathlib import Path
import hashlib
import shutil

VERSION = "v0.2.16"
DIGEST = "4f0b358ec98ec148be9b95cdfb0f0e1a6cbe64da0194fdfac3fffc6f5d1d93e2"
name = f"genvm-universal-{VERSION}.tar.xz"
source = Path.home() / ".cache/genvm-linter" / name
if not source.is_file():
    raise SystemExit("First run: genvm-lint download --version v0.2.16")
with source.open("rb") as stream:
    actual = hashlib.file_digest(stream, "sha256").hexdigest()
if actual != DIGEST:
    raise SystemExit("Official SDK artifact digest mismatch: refusing cache copy")
target = Path.home() / ".cache/gltest-direct" / name
target.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(source, target)
from gltest.direct.sdk_loader import extract_runner
cloudpickle_dir = extract_runner(
    target, "py-lib-cloudpickle",
    "1dlk6mnfabi0z7r39635amyfzw8xb6rm8bv4pmgv6ji1bfx9hghd", VERSION,
)
print("Pinned cloudpickle runner extracted for callback serialization:", cloudpickle_dir)
print("Pinned Direct Mode SDK cache prepared; SHA256 verified")
