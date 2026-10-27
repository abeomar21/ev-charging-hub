"""Let the calcs tests import the scripts by bare name (import assumptions),
the same way the scripts import each other when run as python calcs/<name>.py."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
