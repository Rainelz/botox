import shutil
from pathlib import Path

home = Path.home()

dst_path = home / 'Library' / 'Services'
control_file = dst_path / '.botox'
if not control_file.exists():
    shutil.copytree('resources/workflows/', str(dst_path), dirs_exist_ok=True)
    control_file.touch()
