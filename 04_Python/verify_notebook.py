"""
OLIST - BUILD + HEADLESS-EXECUTE CHECK
=======================================
Rebuilds olist_full_analysis.ipynb, executes a COPY with jupyter nbconvert
(the committed notebook itself stays clean), and asserts zero error cells.

Run:  python 04_Python/verify_notebook.py
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_full_analysis_nb as builder  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
NB = Path(__file__).resolve().parent / "olist_full_analysis.ipynb"


def main():
    builder.build()
    out_dir = Path(tempfile.mkdtemp(prefix="nbcheck_"))
    r = subprocess.run(
        [sys.executable, "-m", "jupyter", "nbconvert", "--to", "notebook",
         "--execute", "--ExecutePreprocessor.timeout=900", str(NB),
         "--output", "executed.ipynb", "--output-dir", str(out_dir)],
        cwd=str(ROOT), capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout)
        print(r.stderr)
        sys.exit("nbconvert execution FAILED")
    exec_path = out_dir / "executed.ipynb"
    nb = json.loads(exec_path.read_text(encoding="utf-8"))
    errors = [c for c in nb["cells"]
              if any(o.get("output_type") == "error" for o in c.get("outputs", []))]
    if errors:
        for c in errors:
            print("ERROR CELL:", "".join(c["source"])[:300])
        sys.exit(f"{len(errors)} error cell(s) in executed notebook")
    n_md = sum(1 for c in nb["cells"] if c["cell_type"] == "markdown")
    n_cd = sum(1 for c in nb["cells"] if c["cell_type"] == "code")
    print(f"OK: {len(nb['cells'])} cells ({n_md} md, {n_cd} code) executed cleanly")
    print("Executed copy:", exec_path)


if __name__ == "__main__":
    main()
