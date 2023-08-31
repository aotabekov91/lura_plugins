import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(Path(BASE_DIR).joinpath('src/plugs')))
sys.path.insert(0, str(Path(BASE_DIR).joinpath('src/modes')))
