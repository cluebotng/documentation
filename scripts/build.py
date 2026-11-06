import os
import sys
from pathlib import Path

from sphinx.cmd.build import build_main

# Only build under a Cloud Native Buildpack (e.g. Toolforge),
# other installs (e.g. GitHub Pages) run sphinx-build themselves
if "CNB_BUILDPACK_DIR" not in os.environ:
    sys.exit(0)

root = Path(__file__).parent.parent
sys.exit(
    build_main(["-n", "-W", "-b", "html", str(root / "source"), str(root / "build")])
)
