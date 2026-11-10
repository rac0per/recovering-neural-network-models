import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def main():
    src = ROOT / "src"
    for source in sorted(src.glob("*.py")):
        compile(source.read_bytes(), str(source), "exec")

    subprocess.run(
        [sys.executable, "-B", str(src / "recover_network.py")],
        cwd=ROOT,
        check=True,
    )


if __name__ == "__main__":
    main()