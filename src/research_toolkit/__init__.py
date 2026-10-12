"""Runnable ports of completed segmentation studies."""
import os
from pathlib import Path

os.environ.setdefault('YOLO_CONFIG_DIR', str(Path('work/runtime/yolo').resolve()))
Path(os.environ['YOLO_CONFIG_DIR']).mkdir(parents=True, exist_ok=True)
os.environ['YOLO_AUTOINSTALL'] = 'false'
__version__ = '0.2.0'
