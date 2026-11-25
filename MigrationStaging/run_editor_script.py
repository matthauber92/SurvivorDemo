"""Preserve the original command line for existing editor launchers."""
from pathlib import Path
import runpy

if __name__ == '__main__':
    runpy.run_path(str(Path(__file__).resolve().parents[1] / 'Tools/Unreal/run_editor_script.py'), run_name='__main__')
